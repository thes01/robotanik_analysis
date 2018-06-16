from Levenshtein import StringMatcher
from ProcessedSubmit import ProcessedSubmit
import re
from sklearn.decomposition import PCA as sklearnPCA
from sklearn.preprocessing import StandardScaler
import numpy as np
import math
from MulticoreTSNE import MulticoreTSNE as TSNE
from parsing import parse_problems
from itertools import groupby
from createRobotanikGraphViewer import createRobotanikGraphViewer
from parseProcessedSubmits import loadProcessedSubmits, getUniqueSumbits

import plotly
from plotly.graph_objs import Scatter, Layout

# target:

# load problem
# load solutions
# do the computing and pca/tsne
# export data to html file with data

PROBLEM_ID = "0654"

# if set to True, then the difference method will compute levensthein distance on visited lists
# otherwise it will compute l. diff. on submits (aka functions)
USE_VISITED = True


def computeDifferentionFromSolutionsMatrix(submits, use_visited: bool):
    """
    for each submit, compute its difference from all solutions,
    so the output matrix is N_SUBMITS x N_SOLUTIONS

    :param submits
    :param use_visited: see global variable USE_VISITED
    :return: difference matrix
    """
    
    solutions = [submit for submit in submits if submit.flowers_left == 0]
    print("{} solutions".format(len(solutions)))

    matrix = np.zeros((len(submits), len(solutions)))
    
    for i in range(len(submits)):
        print(i)

        for s in range(len(solutions)):
            dist = 0
            if use_visited:
                str1 = submits[i].visited_to_unicode(100)
                str2 = solutions[s].visited_to_unicode(100)

                dist = StringMatcher.distance(str1, str2)
            else:
                str1 = submits[i].functions_to_unicode(use_canonized=True)
                str2 = solutions[s].functions_to_unicode(use_canonized=True)

                dist = StringMatcher.distance(str1, str2)

            matrix[i, s] = dist

    return matrix


def computePCA(matrix, use_std_scaler=False):
    sklearn_pca = sklearnPCA(n_components=2)

    if use_std_scaler:
        data_std = StandardScaler().fit_transform(matrix)
        return sklearn_pca.fit_transform(data_std)
    else:
        return sklearn_pca.fit_transform(matrix)

def computeTSNE(matrix, use_std_scaler=False, perplexity=30):
    tsne = TSNE(n_jobs=4, perplexity=perplexity, verbose=1, n_iter=5000)

    if use_std_scaler:
        data_std = StandardScaler().fit_transform(matrix)
        return tsne.fit_transform(data_std)
    else:
        return tsne.fit_transform(matrix)

def getPlotlyData(uniq_submits, y_values, title):
    ns_recursion = {"x": [], "y": [], "text": []}
    ns_normal = {"x": [], "y": [], "text": []}
    s = {"x": [], "y": [], "text": []}
    
    traces = {"ns_recursion" : ns_recursion, "ns_normal": ns_normal, "s": s}

    for i in range(len(uniq_submits)):
        key = ""
        
        if uniq_submits[i].flowers_left == 0:
            key = "s"
        elif uniq_submits[i].maxRecDepth > 300 or len(uniq_submits[i].visited) == 1000:
            key = "ns_recursion"
        else:
            key = "ns_normal"
        
        traces[key]["x"].append(y_values[i][0])
        traces[key]["y"].append(y_values[i][1])

        func_str = ""
        for seq in uniq_submits[i].canonized_functions:
            func_str += seq.__str__() + "|"

        traces[key]["text"].append("{}; {}".format(func_str, uniq_submits[i].metadata['total_times']))

    data = [ 
        Scatter(x=traces["s"]["x"], 
                y=traces["s"]["y"], 
                mode="markers",
                text=traces["s"]["text"],
                name="Solution",
                marker = dict(
                    color = 'rgba(36, 43, 45, .6)',
                )),
        Scatter(x=traces["ns_normal"]["x"], 
                y=traces["ns_normal"]["y"], 
                mode="markers",
                text=traces["ns_normal"]["text"],
                name="No solution",
                marker = dict(
                    color = 'rgba(0, 224, 153, .6)',
                )),
        Scatter(x=traces["ns_recursion"]["x"], 
                y=traces["ns_recursion"]["y"], 
                mode="markers",
                text=traces["ns_recursion"]["text"],
                name="No solution, max recursion exceeded",
                marker = dict(
                    color = 'rgba(247, 195, 56, .6)',
                ))
    ]

    return data

all_problems = parse_problems("data/_zadani.txt")
problem = [p for p in all_problems if p.getFirstId() == PROBLEM_ID][0]

# informative string
info = "Problem #{}".format(PROBLEM_ID)

if USE_VISITED:
    info += "distances to visited list"
else:
    info += "(canonized func) distances to solutions"
        
print(info)

submits = loadProcessedSubmits(PROBLEM_ID)
unique_submits = getUniqueSumbits(submits)
print(len(unique_submits))

# compute the data
matrix = computeDifferentionFromSolutionsMatrix(unique_submits, USE_VISITED)
pca = computePCA(matrix, False)
plotlyData = getPlotlyData(unique_submits, pca, info)

# create HTML file with Robotanik/Plotly view
file_desc = "_" + "visited" if USE_VISITED else ""
createRobotanikGraphViewer(problem, plotlyData, info, "{}_pca".format(file_desc))

# TSNE: 

# for perplexity in [20, 50]:
#     print("Perplexity: {}".format(perplexity))

#     tsne = computeTSNE(matrix, False, perplexity=perplexity)

#     plotlyData = getPlotlyData(unique_submits, tsne, info)
#     # appendUserLinesToPlotlyData(submits, tsne, plotlyData)
#     createRobotanikGraphViewer(problem, plotlyData, info, "{}_tsne_diff_to_solutions_p_{}".format(file_desc, perplexity))