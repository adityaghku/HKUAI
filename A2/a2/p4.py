import sys, parse
import time, os, copy, math

import random

from p1 import (
    printState,
    initialPacmanLoc,
    pacmanAlive,
    moveAgent,
    manhattanDistance,
    allPellets,
    deepcopy,
)

from p3 import noPellets, initialGhostLocs, validMoves


#Multi ghost eval function
def evaluationF(pacmanLoc, ghostLoc, state, score):

    if allPellets(state):
        #print(int(not pacmanAlive(state)))
        if abs(score[0]) > 100:
            return (
                score[0] / (10 ** (len(str(score[0])) - 2)) #we dont want score to dominate decision and get infinite loop
                + -2
                / min(
                    [manhattanDistance(pacmanLoc, x) + 0.1 for y, x in ghostLoc.items()]
                )
                - 8 * min([manhattanDistance(pacmanLoc, x) for x in allPellets(state)])
                - 10 * len(allPellets(state))
                - (10 ** 10) * int(not pacmanAlive(state))
            )
        
        else:
            return (
                score[0]
                + -2
                / min(
                    [manhattanDistance(pacmanLoc, x) + 0.1 for y, x in ghostLoc.items()]
                )
                - 4 * min([manhattanDistance(pacmanLoc, x) for x in allPellets(state)])
                - 10 * len(allPellets(state))
                - (10 ** 10) * int(not pacmanAlive(state))
            )

    return math.inf


def better_play_mulitple_ghosts(problem):

    seed, allMoves, state = problem
    # random.seed(seed, version=1)

    pacmanLoc = initialPacmanLoc(state)
    ghostLoc = initialGhostLocs(state)
    previousPacmanMove = [] #Prevent infinite loop

    numberOfAgents = len(ghostLoc) + 1

    ghostOnPellet = []
    for i in range(numberOfAgents - 1):
        ghostOnPellet.append([False])

    moveCounter = 1

    score = [0]

    ans = ""
    ans += "seed: " + str(int(seed)) + "\n"
    ans += str(score[0]) + "\n"
    ans += printState(state)
    
    # Same as p2.py with multiple ghost case
    while not noPellets(state, ghostOnPellet) and pacmanAlive(state):
        
        if (moveCounter - 1) % numberOfAgents == 0:
            
            evalMove = ""
            currentMaxScore = -math.inf
            
            for move in validMoves(state, pacmanLoc[0], pacmanLoc[1]):
                
                evalMoveScores = evaluationF(
                    moveAgent(
                        deepcopy(state),
                        pacmanLoc.copy(),
                        move,
                        score.copy(),
                        ghostOnPellet.copy(),
                    )[1].copy(),
                    ghostLoc.copy(),
                    moveAgent(
                        deepcopy(state),
                        pacmanLoc.copy(),
                        move,
                        score.copy(),
                        ghostOnPellet.copy(),
                    )[0],
                    score.copy(),
                )
                if len(previousPacmanMove) > 2:
                    if move == previousPacmanMove[-2]:
                        evalMoveScores = -math.inf + 1

                if evalMoveScores > currentMaxScore:
                    evalMove = move
                    currentMaxScore = evalMoveScores
            
            
            #prevent infinite loop to some extent
            if moveCounter > 10000:
                if random.randint(0, 10) == 9:
                    #print(validMoves(state, pacmanLoc[0], pacmanLoc[1]))
                    evalMove = random.choice(validMoves(state, pacmanLoc[0], pacmanLoc[1]))
            
            
            previousPacmanMove += [evalMove]
            #print(evalMove)
            ans += str(moveCounter) + ": P moving " + str(evalMove) + "\n"

            score[0] -= 1

            state, pacmanLoc = moveAgent(
                state, pacmanLoc, evalMove, score, ghostOnPellet
            )

            ans += printState(state)

            if noPellets(state, ghostOnPellet) and pacmanAlive(state):
                score[0] += 500

            ans += "score: " + str(score[0]) + "\n"

        elif (moveCounter - 1) % numberOfAgents == 1:

            temp = validMoves(state, ghostLoc["W"][0], ghostLoc["W"][1])

            if temp:
                randomMove = random.choice(temp)
                ans += str(moveCounter) + ": W moving " + str(randomMove) + "\n"
                state, ghostLoc["W"] = moveAgent(
                    state, ghostLoc["W"], randomMove, score, ghostOnPellet[0]
                )
                ans += printState(state)
                ans += "score: " + str(score[0]) + "\n"

            else:
                ans += str(moveCounter) + ": W moving " + "\n"
                ans += printState(state)
                ans += "score: " + str(score[0]) + "\n"

        elif numberOfAgents >= 3 and (moveCounter - 1) % numberOfAgents == 2:

            temp = validMoves(state, ghostLoc["X"][0], ghostLoc["X"][1])

            if temp:
                randomMove = random.choice(temp)
                ans += str(moveCounter) + ": X moving " + str(randomMove) + "\n"
                state, ghostLoc["X"] = moveAgent(
                    state, ghostLoc["X"], randomMove, score, ghostOnPellet[1]
                )
                ans += printState(state)
                ans += "score: " + str(score[0]) + "\n"

            else:
                ans += str(moveCounter) + ": X moving " + "\n"
                ans += printState(state)
                ans += "score: " + str(score[0]) + "\n"

        elif numberOfAgents >= 4 and (moveCounter - 1) % numberOfAgents == 3:

            temp = validMoves(state, ghostLoc["Y"][0], ghostLoc["Y"][1])

            if temp:
                randomMove = random.choice(temp)
                ans += str(moveCounter) + ": Y moving " + str(randomMove) + "\n"
                state, ghostLoc["Y"] = moveAgent(
                    state, ghostLoc["Y"], randomMove, score, ghostOnPellet[2]
                )
                ans += printState(state)
                ans += "score: " + str(score[0]) + "\n"

            else:
                ans += str(moveCounter) + ": Y moving " + "\n"
                ans += printState(state)
                ans += "score: " + str(score[0]) + "\n"

        else:

            temp = validMoves(state, ghostLoc["Z"][0], ghostLoc["Z"][1])

            if temp:
                randomMove = random.choice(temp)
                ans += str(moveCounter) + ": Z moving " + str(randomMove) + "\n"
                state, ghostLoc["Z"] = moveAgent(
                    state, ghostLoc["Z"], randomMove, score, ghostOnPellet[3]
                )
                ans += printState(state)
                ans += "score: " + str(score[0]) + "\n"

            else:
                ans += str(moveCounter) + ": Z moving " + "\n"
                ans += printState(state)
                ans += "score: " + str(score[0]) + "\n"

        moveCounter += 1

    if pacmanAlive(state):
        ans += "WIN: Pacman"
        return ans, "Pacman"

    else:
        ans += "WIN: Ghost"
        return ans, "Ghost"


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 4
    file_name_problem = str(test_case_id) + ".prob"
    file_name_sol = str(test_case_id) + ".sol"
    path = os.path.join("test_cases", "p" + str(problem_id))
    problem = parse.read_layout_problem(os.path.join(path, file_name_problem))
    num_trials = int(sys.argv[2])
    verbose = bool(int(sys.argv[3]))
    print("test_case_id:", test_case_id)
    print("num_trials:", num_trials)
    print("verbose:", verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = better_play_mulitple_ghosts(copy.deepcopy(problem))
        if winner == "Pacman":
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count / num_trials * 100
    end = time.time()
    print("time: ", end - start)
    print("win %", win_p)
