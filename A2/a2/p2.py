import sys, parse
import time, os, copy

import random, math

from p1 import *

# Evauation func for single ghost case
def evaluationF(pacmanLoc, ghostLoc, state, score):

    if allPellets(state):

        return (
            score[0] / (10 ** len(str(score[0])) - 2)
            + -2 / (manhattanDistance(pacmanLoc, ghostLoc) + 1)
            - 2.5 * min([manhattanDistance(pacmanLoc, x) for x in allPellets(state)])
            - 10 * len(allPellets(state))
            - (10 ** 10) * int(not pacmanAlive(state))
        )

    return math.inf


#same code as p1.py but we loop through all possible moves and pick move with highest evalF
#copy and deepcopy are used to check the vals of all other states

def better_play_single_ghosts(problem):
    seed, allMoves, state = problem
    # random.seed(seed, version=1)

    pacmanLoc = initialPacmanLoc(state)
    ghostLoc = initialGhostLoc(state)

    previousPacmanMove = []

    moveCounter = 1

    score = [0]

    ghostOnPellet = [False]

    ans = ""
    ans += "seed: " + str(int(seed)) + "\n"
    ans += str(score[0]) + "\n"
    ans += printState(state)

    while not noPellets(state, ghostOnPellet) and pacmanAlive(state):

        if moveCounter % 2 == 1:

            evalMove = ""
            currentMaxScore = -math.inf
            #print(printState(state))
            for move in validMoves(state, pacmanLoc[0], pacmanLoc[1]):
                # print(validMoves(state, pacmanLoc[0], pacmanLoc[1]))
                evalMoveScores = evaluationF(
                    moveAgent(
                        deepcopy(state),
                        pacmanLoc.copy(),
                        move,
                        score.copy(),
                        ghostOnPellet.copy(),
                    )[1],
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
            # print(evalMove)
            
            if moveCounter > 10000:
                if random.randint(0, 10) == 10:
                    evalMove = random.choice(validMoves(state, pacmanLoc[0], pacmanLoc[1]))
            
            previousPacmanMove += [evalMove]

            ans += str(moveCounter) + ": P moving " + str(evalMove) + "\n"

            score[0] -= 1

            state, pacmanLoc = moveAgent(
                state, pacmanLoc, evalMove, score, ghostOnPellet
            )

            ans += printState(state)

            if noPellets(state, ghostOnPellet) and pacmanAlive(state):
                score[0] += 500

            ans += "score: " + str(score[0]) + "\n"

        if moveCounter % 2 == 0:

            randomMove = random.choice(validMoves(state, ghostLoc[0], ghostLoc[1]))

            ans += str(moveCounter) + ": W moving " + str(randomMove) + "\n"

            state, ghostLoc = moveAgent(
                state, ghostLoc, randomMove, score, ghostOnPellet
            )

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
    problem_id = 2
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
        solution, winner = better_play_single_ghosts(copy.deepcopy(problem))
        if winner == "Pacman":
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count / num_trials * 100
    end = time.time()
    print("time: ", end - start)
    print("win %", win_p)
