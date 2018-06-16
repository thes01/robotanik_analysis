
def visited_sets_difference(first: set, second: set):
    diff = 0
    # in first, not in second
    for field in first:
        if field not in second:
            diff += 1
    for field in second:
        if field not in first:
            diff += 1
    return diff


# def computeDifferentionMatrix(submits, features, n_features):
#     COUNT_VISITED_MAX_LENGTH = 100

#     matrix = np.zeros((len(submits), len(submits) * n_features))
#     i = 0

#     for y in range(len(submits)):
#         print(y)
        
#         for x in range(y + 1, len(submits)):
#             delta = 0
            
#             diff_f_steps = abs(submits[y].Fsteps - submits[x].Fsteps)
#             diff_lr_steps = abs(submits[y].LRsteps - submits[x].LRsteps)
            
#             if features['f_steps']:
#                 matrix[y, x * n_features + delta] = diff_f_steps
#                 matrix[x,y * n_features + delta] = diff_f_steps
                
#                 delta += 1
#             if features['lr_steps']:
#                 matrix[y, x * n_features + delta] = diff_lr_steps
#                 matrix[x,y * n_features + delta] = diff_lr_steps
                
#                 delta += 1        
#             if features['flr_steps_ratio']:
#                 ratio = diff_f_steps if diff_lr_steps == 0 else diff_f_steps / diff_lr_steps
                
#                 matrix[y, x * n_features + delta] = ratio
#                 matrix[x,y * n_features + delta] = ratio
                
#                 delta += 1   
                
#             if features['max_recursion']:
#                 matrix[y, x * n_features + delta] = abs(submits[y].maxRecDepth - submits[x].maxRecDepth)
#                 matrix[x,y * n_features + delta] = abs(submits[y].maxRecDepth - submits[x].maxRecDepth)
                
#                 delta += 1  
                
#             if features['log(max_recursion)']:
#                 diff = abs(submits[y].maxRecDepth - submits[x].maxRecDepth)
#                 log = math.log(diff) if diff > 0 else 0
                
#                 matrix[y, x * n_features + delta] = log
#                 matrix[x,y * n_features + delta] = log
                
#                 delta += 1   
                
#             if features['flowers_left']:
#                 matrix[y, x * n_features + delta] = abs(submits[y].flowers_left - submits[x].flowers_left)
#                 matrix[x,y * n_features + delta] = abs(submits[y].flowers_left - submits[x].flowers_left)
                
#                 delta += 1  
                
#             if features['stack_left']:
#                 matrix[y, x * n_features + delta] = abs(submits[y].stackLeft - submits[x].stackLeft)
#                 matrix[x,y * n_features + delta] = abs(submits[y].stackLeft - submits[x].stackLeft)
                
#                 delta += 1 

#             if features['recolored']:
#                 matrix[y, x * n_features + delta] = abs(submits[y].recoloredCount - submits[x].recoloredCount)
#                 matrix[x,y * n_features + delta] = abs(submits[y].recoloredCount - submits[x].recoloredCount)
                
#                 delta += 1
                
#             if features['log(stack_left)']:
#                 diff = abs(submits[y].stackLeft - submits[x].stackLeft)
#                 log = math.log(diff) if diff > 0 else 0
                
#                 matrix[y, x * n_features + delta] = log
#                 matrix[x,y * n_features + delta] = log
                
#                 delta += 1 
                
#             if features['function_strings']:
#                 str1 = submits[y].functions_to_unicode(False)
#                 str2 = submits[x].functions_to_unicode(False)
                
#                 dist = StringMatcher.distance(str1, str2)
                        
#                 matrix[y, x * n_features + delta] = dist
#                 matrix[x,y * n_features + delta] = dist
                
#                 delta += 1  
                
#             if features['canonized_strings']:
#                 str1 = submits[y].functions_to_unicode(True)
#                 str2 = submits[x].functions_to_unicode(True)
                
#                 dist = StringMatcher.distance(str1, str2)
                        
#                 matrix[y, x * n_features + delta] = dist
#                 matrix[x,y * n_features + delta] = dist
                
#                 delta += 1
                
#             if features['visited_sequence']:
#                 str1 = submits[y].visited_to_unicode(COUNT_VISITED_MAX_LENGTH)
#                 str2 = submits[x].visited_to_unicode(COUNT_VISITED_MAX_LENGTH)
                
#                 dist = StringMatcher.distance(str1, str2)
                        
#                 matrix[y, x * n_features + delta] = dist
#                 matrix[x,y * n_features + delta] = dist
                
#                 delta += 1

#             if features['visited_set']:
#                 diff = visited_sets_difference(submits[x].getVisitedSet(), submits[y].getVisitedSet())

#                 matrix[y, x * n_features + delta] = diff
#                 matrix[x,y * n_features + delta] = diff

#                 delta += 1

#     return matrix



# def appendUserLinesToPlotlyData(submits, y_values, plotly_data):
#     users = groupby(submits, lambda s: s.metadata['user_id'])

#     for user_id, user in groupby(submits, lambda s: s.metadata['user_id']):
#         user_trace = {"x": [], "y": []}

#         for submit in user:
#             last_unique_index = -1

#             if submit.metadata['unique_index'] != last_unique_index:
#                 last_unique_index = submit.metadata['unique_index']
#                 user_trace["x"].append(y_values[last_unique_index][0])
#                 user_trace["y"].append(y_values[last_unique_index][1])

#         scatter = Scatter(x=user_trace["x"], 
#                 y=user_trace["y"], 
#                 name="User {}".format(user_id),
#                 # visible="legendonly",
#                 mode="lines",
#                 marker = dict(
#                     color = 'rgba(100, 100, 100, .1)'
#                 ))
        
#         plotly_data.append(scatter)





n_features = 0
# features = {
#         'f_steps': True,
#         'lr_steps': True,
#         'flr_steps_ratio': False,
#         'max_recursion': False,
#         'log(max_recursion)': False,
#         'flowers_left': False,
#         'stack_left': False,
#         'log(stack_left)': True,
#         'recolored': True,
#         'function_strings': False,
#         'canonized_strings': False,
#         'visited_sequence': False,
#         'visited_set': True
#     }

# for name, count_feature in features.items():
#     if count_feature:
#         n_features += 1
#         info += ", " + name




def testCanonizeEquivalence(problem, submits):
    for i in range(len(submits)):
        if i == len(submits) - 2:
            continue
            
        can, siminfo = canonize(problem, submits[i])

    return True