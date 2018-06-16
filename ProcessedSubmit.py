from Problem import Problem
from structures import *
from simulation import *
from canonize import *


class ProcessedSubmit:
    def __init__(self, time: int, original_functions: list, canonized_functions: list,
                 flowers_left: int, Fsteps: int, LRsteps: int, maxRecDepth: int, visited: list,
                 stackLeft, recoloredCount: int, total_time: int):

        self.time = time

        self.original_functions = original_functions
        self.canonized_functions = canonized_functions

        self.flowers_left = flowers_left
        self.Fsteps = Fsteps
        self.LRsteps = LRsteps
        self.maxRecDepth = maxRecDepth
        self.visited = visited
        self.visited_set = None
        self.stackLeft = stackLeft
        self.recoloredCount = recoloredCount
        self.total_time = total_time

        # for various purposes during processing and making them unique
        self.metadata = {}

    @classmethod
    def parseFromStr(cls, parse_str: str):
        values = parse_str.split(';')

        time = (int)(values[0])

        original_sequences = values[1].split('|')
        canonized_sequences = values[2].split('|')
        original_functions = [Sequence(i + 1, original_sequences[i]) for i in range(5)]
        canonized_functions = [Sequence(i + 1, canonized_sequences[i]) for i in range(5)]

        flowers_left = (int)(values[3])
        Fsteps = (int)(values[4])
        LRsteps = (int)(values[5])
        maxRecDepth = (int)(values[6])
        visited = []

        for t in values[7].split(','):
            if len(t) > 1:
                xy = t.split('-')
                visited.append((xy[0], xy[1]))

        # later added values, may not be compatible
        stackLeft = 0
        recoloredCount = 0
        total_time = 0

        if len(values) > 8:
            stackLeft = int(values[8])

        if len(values) > 9:
            recoloredCount = int(values[9])

        if len(values) > 10:
            total_time = int(values[10])

        return cls(time, original_functions, canonized_functions,
                   flowers_left, Fsteps, LRsteps,
                   maxRecDepth, visited, stackLeft, recoloredCount, total_time)

    @classmethod
    def computeFromSubmit(cls, problem: Problem, submit: Submit, total_time: int):
        canonized, siminfo = canonize(problem, submit)

        return cls(submit.time, submit.functions, canonized.functions,
                   siminfo.flowersLeft, siminfo.Fsteps, siminfo.LRsteps,
                   siminfo.maxRecDepth, siminfo.visited, siminfo.stackLeft,
                   siminfo.recoloredCount, total_time)

    def getVisitedSet(self):
        if self.visited_set is None:
            self.visited_set = set(self.visited)

        return self.visited_set

    # helper functions
    def visited_to_unicode(self, max_len=50):
        unicode_str = ""
        count = 0
        
        for i in range(len(self.visited)):
            if count > max_len:
                break
            
            unicode_str += chr(int(self.visited[i][0]) + 16 * int(self.visited[i][1]))
            count += 1

        return unicode_str

    def functions_to_unicode(self, use_canonized: bool):
        unicode_str = ""

        arr = self.canonized_functions if use_canonized else self.functions

        for seq in arr:
            for move in seq.moves:
                # unicode_str += chr(20 + ord(move.condition)) + chr(10 * ord(move.action))
                unicode_str += chr(20 + ord(move.condition) + 10 * ord(move.action))
            unicode_str += chr(19)

        return unicode_str

    def __str__(self):
        orig_str = ""
        canon_str = ""
        visited_str = ""

        for seq in self.original_functions:
            orig_str += seq.__str__() + "|"

        for seq in self.canonized_functions:
            canon_str += seq.__str__() + "|"

        for xy in self.visited:
            visited_str += "{}-{},".format(xy[0], xy[1])

        return "{};{};{};{};{};{};{};{};{};{};{}".format(self.time, orig_str,
                                             canon_str, self.flowers_left,
                                             self.Fsteps, self.LRsteps,
                                             self.maxRecDepth, visited_str,
                                             self.stackLeft, self.recoloredCount,
                                             self.total_time)

    def __repr__(self):
        return self.__str__()
