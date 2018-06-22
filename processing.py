import re
from simulation import *
from structures import User, Game, Sequence, Move
import Problem
import Submit
from ProcessedSubmit import ProcessedSubmit
from canonize import *
from parsing import *
from operator import xor
import sys
import os.path

# log source data folder
SRC_DATA_FOLDER = "data/current"
PROCESSED_DATA_FOLDER = "data/processed"

# append _old suffix when processing the old data
file_suffix = ""
if SRC_DATA_FOLDER == "data/old":
    file_suffix = "_old"

# specify which problems are to process
problems = [p for p in parse_problems('data/_zadani.txt') if p.getFirstId() == '0651']


for problem in problems:
    print("problem", problem.getFirstId())
    srcFilePath = "{}/{}.txt".format(SRC_DATA_FOLDER, problem.getFirstId())

    if not os.path.exists(srcFilePath):
        print("problem file {} not found".format(srcFilePath))
        continue
    
    # parse the users objects (containing all their submits)
    users = parse_gamelog(srcFilePath)

    procFilePath = "{}/{}{}.txt".format(PROCESSED_DATA_FOLDER, problem.getFirstId(), file_suffix)

    with open(procFilePath, 'w') as export:
        for user in users:
            # filter out users with few submits
            if user.submitCount() <= 4:
                continue

            export.write("user {}\n".format(user.uid))
            print("user ", user.uid)

            total_time = 0

            for game in user.games:
                for submit in game.submits:
                    # filter out last submits that are marked as solutions
                    # (just duplicates of the precedent ones)
                    if submit is game.submits[-1] and submit.is_solution:
                        continue

                    total_time += submit.time

                    export.write("{}\n".format(ProcessedSubmit.computeFromSubmit(problem, submit, total_time)))
