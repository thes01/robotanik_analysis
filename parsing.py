import re
from simulation import *
from structures import User, Game, Sequence, Move
import Problem
import Submit
from canonize import *
from operator import xor
import sys

def parse_problems(filename):
    f = open(filename, "r")
    s = f.read()
    s = s.split("\n\n")[1:]  # strip the first line
    f.close()

    problems = []

    for paragraph in s:
        if len(paragraph) > 0:
            problems.append(Problem(paragraph))

    return problems


def parse_gamelog(problemId=None, path='data/'):
    """
    parse gamelog and return list of users

    :param problemId: id (as string) of problem to process
    :param path: path to directory with logs
    :return: list of users
    """

    users = []
    firstLine = True
    currentUser = None

    for line in f:
        if firstLine:
            # First line contains the name of the problem, which can be arbitrary and can therefore interfere
            # with conditions below. For example the problem "960" interferes with if re.match("\d",line)
            firstLine = False
            continue
        if re.search("User", line):
            uid = int(line.rstrip().split()[-1])
            currentUser = User(uid)
            users.append(currentUser)

        if re.search("Game", line):
            currentUser.games.append(Game())

        if re.match("\d", line):
            currentUser.games[-1].submits.append(Submit.parsedFromStr(line))

    return users


