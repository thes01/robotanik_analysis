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



problems = [p for p in parse_problems('data/_zadani.txt') if p.getFirstId() == '0663']

# problem = [p for p in problems if p.getFirstId() == '0680'][0]


for problem in problems:
    print("problem", problem.id)

    if not os.path.exists("data/old/{}.txt".format((problem.getFirstId()))):
        print("problem file {} not found".format(problem.getFirstId()))
        continue
    
    users = parse_gamelog(path='data/old/', problemId=problem.getFirstId())

    with open('data/processed_new/{}_old.txt'.format(problem.getFirstId()), 'w') as export:
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
