from structures import *
from simulation import *
from copy import deepcopy


def canonize(problem, sub: Submit, testEquivalence=False):
    '''
    canonize submit according to given problem
    :param problem:
    :param sub: submit to canonize
    :return: canonized form
    '''

    # deep copy to prevent changing original submit
    submit = deepcopy(sub)
    submit.sortFunctions()

    canonized = Submit.empty()
    canonized.is_solution = submit.is_solution

    simulationInfo = simulate(problem, submit)   # simulates the submit to get simulation information

    for i in range(5):
        if not simulationInfo.functionsExecuted[i]:
            # remove functions that were not executed - set as empty
            submit.functions[i] = Sequence(i + 1, "")

    for sequence in submit.functions:
        # remove commands that were not executed
        # attention - moves in simulationInfo must be the same as moves in sequence !
        sequence.moves = [move for move in sequence.moves if move in simulationInfo.movesExecuted]

        # remove conditions that were always true
        for move in sequence.moves:
            if move.condition != "_" and move not in simulationInfo.conditionWasFalse:
                move.condition = "_"

    for sequence in submit.functions:
        i = 0
        while i < len(sequence.moves):
            move = sequence.moves[i]
            if i < len(sequence.moves) - 1:
                move2 = sequence.moves[i + 1]
                #   #  LL to RR
                if move.equals(move2) and move.action == "L":
                    move.action = "R"
                    sequence.moves[i + 1] = move
                # remove LR / RL
                elif move.condition == move2.condition and move.action in "LR" and move2.action in "LR" and move.action != move2.action:
                    sequence.deleteMoves([i, i+1])

                    if (i > 0):
                        i -= 1
                    continue
            # remove empty functions
            if move.action.isdigit() and submit.functions[int(move.action)-1].is_empty:
                sequence.deleteMoves([i])
                if (i > 0): i -= 1

                continue
            # remove recoloring green to green, red to red, ...
            if move.action == move.condition:
                sequence.deleteMoves([i])
                if (i > 0): i -= 1

                continue
            i += 1

        canonized.appendFunction(sequence)

    
    if submit.equalsByFunctions(canonized):
        # simulate the canonized version
        if testEquivalence:
            canSimulationInfo = simulate(problem, canonized)

            if not simulationInfo.equals(canSimulationInfo):
                print("submit / canonized not equivalent")

        return (canonized, simulationInfo)
    else:
        #  if submit changed, run canonization again (there is probably something more to canonize)
        return canonize(problem, canonized)
