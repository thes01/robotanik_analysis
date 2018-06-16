from Problem import Problem
from structures import *
from simulation import *
from copy import deepcopy


# 6;42;solution:_L_FgRgRgF_1|||||
class Submit:
    def __init__(self, time, is_solution, functions):
        self.time = time
        self.is_solution = is_solution
        self.functions = functions

    @classmethod
    def parsedFromStr(cls, parse_str):
        data = parse_str.split(';')

        ending = data[2].split(':')
        func_data = ending[-1].split('|')

        time = int(data[1])
        is_solution = ending[0] == 'solution'
        functions = [Sequence(i + 1, func_data[i]) for i in range(5)]

        return cls(time, is_solution, functions)

    @classmethod
    def empty(cls):
        return cls(0, False, [])

    def sortFunctions(self):
        for func in self.functions:
            swapped = True
            while swapped:
                swapped = False
                for i in range(len(func.moves)-1):
                    move1 = func.moves[i]
                    move2 = func.moves[i + 1]
                    #  if adjacent commands are both rotations
                    if move1.action in "LR" and move2.action in "LR":
                        #  r < g < b < - and with same condition R<L
                        if move1.condition < move2.condition or (move1.condition == move2.condition and move1.action == "L" and move2.action == "R"):
                            func.moves[i], func.moves[i + 1] = move2, move1
                            swapped = True

    def appendFunction(self, sequence):
        self.functions.append(sequence)

    def equalsByFunctions(self, submit):
        if len(self.functions) != len(submit.functions):
            return False

        for i in range(len(self.functions)):
            if not self.functions[i].equalsByMoves(submit.functions[i]):
                return False

        return True

    def __str__(self):
        ret = "canonized " if self.time == 0 else ""

        if self.is_solution:
            ret += "solution:"

        for function in self.functions:
            for move in function.moves:
                ret += move.__str__() 

            ret += "|"

        return ret

    def __repr__(self):
        return self.__str__()
