from structures import Move


class SimulationInfo:
    def __init__(self):
        self.maxRecDepth = 0
        self.Fsteps = 0
        self.LRsteps = 0
        self.functionsExecuted = [True, False, False, False, False]
        self.functionsOrdering = [1, 9, 9, 9, 9]
        self.movesExecuted = set()
        self.conditionWasFalse = set()
        self.visited = []
        self.flowersLeft = 0
        self.stackLeft = 0
        self.recoloredCount = 0

    def getVisitedSet(self):
        return set(self.visited)

    def isSolved(self):
        return self.flowersLeft == 0 and self.Fsteps > 0

    def equals(self, siminfo):
        _steps_eq = self.Fsteps == siminfo.Fsteps and self.LRsteps == siminfo.LRsteps
        _visited_eq = self.visited == siminfo.visited
        _flowers_eq = self.flowersLeft == siminfo.flowersLeft
        _recolored_eq = self.recoloredCount == siminfo.recoloredCount

        return _steps_eq and _visited_eq and _flowers_eq and _recolored_eq

    def __str__(self):
        solved = "solved" if self.isSolved() else "unsolved, flowers left: " + str(self.flowersLeft)

        return solved
