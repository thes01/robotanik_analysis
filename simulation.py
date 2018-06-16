from colorconsole import terminal   # just for visualization, not necessary for analyses
from time import sleep   # just for visualization, not necessary for analyses
from structures import *
from SimulationInfo import SimulationInfo
from Problem import Problem
from Submit import Submit


def simulate(problem: Problem, submit: Submit):
    '''
    simulates given solution of the problem, animation works only when run from command line
    :param problem:
    :param solution:
    :return: dictionary with simulation information
    '''

    board = problem.getBoardCopy()
    flowersLeft = problem.getFlowerCount()

    simInfo = SimulationInfo()
    
    # current recursion depth
    recDepth = 0

    # ordering of functions - number which will be associated  with the next function run
    # F1 must alway be F1, so we start from 2
    order = 2
    
    col = problem.robotCol
    row = problem.robotRow
    rot = problem.robotDir
    simInfo.visited.append((row, col))   # visited fields
    
    moves = list(reversed(submit.functions[0].moves))   # stack of steps to simulate
    stack = [[1, 0]]   # stack of functions and positions of simulated steps
    # while there are flowers and steps to make, make a step, maximum is 1000 steps, plus max 5000 steps to go (to avoid recursion without any moving)
    while (moves != [] and flowersLeft > 0 and len(simInfo.visited) < 1000 and len(moves) < 5000):
        move = moves[-1]
        moves.pop()

        # find the function and position of simulated step
        actf, actp = stack[-1]

        # if recursion is ending, pop from stack
        if move.action in "vt":
            stack.pop()
        # otherwise move to next position in the same function
        else:
            stack[-1][1] += 1

        # if the color of current field is the same as the condition or there is no condition
        if move.condition == board[row][col] or move.condition == "_":
            if move.action != "v" and move.action != "t":
                # if it is the actual command (not the info about recursion ending) set the command to executed
                # command is not considered executed if it is recoloring to the same color
                if move.action != board[row][col]:
                    simInfo.movesExecuted.add(move)
            if move.action.isdigit():
                # if the command is F1 - F5
                if moves != [] and moves[-1].action != "v" and moves[-1].action != "t":
                    # if its not the tail recursion
                    recDepth += 1   # increase recursion depth
                    # update maximum recursion depth
                    simInfo.maxRecDepth = max(recDepth, simInfo.maxRecDepth) 
                    moves.append(Move("_v"))
                else: moves.append(Move('_t'))   # otherwise it is tail rec - append info about tail rec ending

                moves += list(reversed(submit.functions[int(move.action)-1].moves))   # add commands from called function on steps stack
                stack.append([int(move.action), 0])   # add first position of function on the top of positions stack
                simInfo.functionsExecuted[int(move.action)-1] = True   # function was executed right now

                # if function was not executed before, set its execution order
                if simInfo.functionsOrdering[int(move.action)-1] == 9:
                    simInfo.functionsOrdering[int(move.action)-1] = order
                    order += 1
            else:
                # command is NOT a function call
                if move.action == "v":
                    # recursion ended - decrease depth
                    recDepth -= 1 
                if move.action == "L":
                    # rotate left and increase LR steps
                    rot=(rot-1) % 4
                    simInfo.LRsteps += 1
                    simInfo.visited.append((row, col))
                if move.action == "R":
                    # rotate right and increase LR steps
                    rot=(rot+1) % 4
                    simInfo.LRsteps += 1
                    simInfo.visited.append((row, col))
                if move.action == "F":
                    # move in the direction given by rotation
                    col+=[1,0,-1,0][rot]
                    row+=[0,1,0,-1][rot]

                    if row < 0 or row >= len(board):
                        break
                    if col < 0 or col >= len(board[row]):
                        break
                    if board[row][col] == " ":
                        break

                    simInfo.Fsteps += 1
                    simInfo.visited.append((row, col))
                        
                if move.action in "rgb":
                    # recolor if necessary
                    if board[row][col] != move.action:
                        board[row] = board[row][0:col]+move.action+board[row][col+1:]
                        simInfo.recoloredCount += 1
                if board[row][col].istitle():
                    # if there was a flower, it is now taken
                    board[row] = board[row][0:col]+board[row][col].lower()+board[row][col+1:]
                    flowersLeft -= 1
        else:
            # command was not executed because the condition was False
            # therefore this condition was useful
            simInfo.conditionWasFalse.add(move)
            
    simInfo.stackLeft = recDepth   # save recursion depth at the end of simulation
    simInfo.flowersLeft = flowersLeft
    return simInfo
