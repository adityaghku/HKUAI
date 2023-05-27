import sys, parse
import time, os, copy, math, random

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
from p4 import evaluationF

#Minimax implementation
def minimax(
    agent, depth, moveCounter, state, pacmanLoc, ghostLoc, ghostOnPellet, score
):

    if noPellets(state, ghostOnPellet) or (not pacmanAlive(state)) or depth > k:
        return evaluationF(
            pacmanLoc.copy(), ghostLoc.copy(), deepcopy(state), score.copy()
        )

    newAgent = agent + 1

    if newAgent == numberOfAgents:
        newAgent = 0

    if newAgent == 0:
        depth += 1

    if newAgent == 0:

        maxScore = -math.inf  # arbitrary high number

        for move in validMoves(state, pacmanLoc[0], pacmanLoc[1]):

            tempState, tempAgent = moveAgent(
                deepcopy(state),
                pacmanLoc.copy(),
                move,
                score.copy(),
                deepcopy(ghostOnPellet),
            )

            currentScore = minimax(
                1,
                depth,
                moveCounter,
                tempState,
                tempAgent,
                ghostLoc.copy(),
                deepcopy(ghostOnPellet),
                score.copy(),
            )

            if maxScore < currentScore:
                maxScore = currentScore

        return maxScore

    else:

        ghostIdentifier = ghosts[newAgent - 1]

        minScore = math.inf

        for move in validMoves(
            state, ghostLoc[ghostIdentifier][0], ghostLoc[ghostIdentifier][1]
        ):

            tempAgent = ghostLoc.copy()
            tempState, tempAgent[ghostIdentifier] = moveAgent(
                deepcopy(state),
                ghostLoc[ghostIdentifier].copy(),
                move,
                score.copy(),
                deepcopy(ghostOnPellet),
            )

            currentScore = minimax(
                newAgent,
                depth,
                moveCounter,
                tempState,
                pacmanLoc.copy(),
                tempAgent,
                deepcopy(ghostOnPellet),
                score.copy(),
            )
            
            if minScore > currentScore:
                minScore = currentScore

        return minScore


def min_max_mulitple_ghosts(problem, k):
    seed, allMoves, state = problem
    # random.seed(seed, version=1)

    pacmanLoc = initialPacmanLoc(state)
    ghostLoc = initialGhostLocs(state)
    previousPacmanMove = []

    global ghosts
    ghosts = ["W", "X", "Y", "Z"]

    global numberOfAgents
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
    
    # Same as p4.py but we call minimax instead of evalF
    while ((not noPellets(state, ghostOnPellet)) and pacmanAlive(state)):

        if (moveCounter - 1) % numberOfAgents == 0:
            evalMove = random.choice(validMoves(state, pacmanLoc[0], pacmanLoc[1]))
            maxevalMoveScore = -math.inf

            for move in validMoves(state, pacmanLoc[0], pacmanLoc[1]):
                
                tempState, tempAgent = moveAgent(
                    deepcopy(state),
                    pacmanLoc.copy(),
                    move,
                    score.copy(),
                    deepcopy(ghostOnPellet),
                )

                evalMoveScores = minimax(
                    0,
                    k,
                    moveCounter,
                    tempState,
                    tempAgent,
                    ghostLoc.copy(),
                    deepcopy(ghostOnPellet),
                    score.copy(),
                )

                if len(previousPacmanMove) > 2:
                    if move == previousPacmanMove[-2]:
                        evalMoveScores = -math.inf

                if evalMoveScores > maxevalMoveScore:
                    evalMove = move
                    maxevalMoveScore = evalMoveScores
            
            if moveCounter > 10000:
                if random.randint(0, 10) == 9:
                    #print(validMoves(state, pacmanLoc[0], pacmanLoc[1]))
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

        elif (moveCounter - 1) % numberOfAgents == 1:

            temp = validMoves(state, ghostLoc["W"][0], ghostLoc["W"][1])

            if temp:

                # Should be renamed
                randomMove = ""
                minevalMoveScore = math.inf
                for move in temp:
                    
                    tempAgent = ghostLoc.copy()
                    tempState, tempAgent["W"] = moveAgent(
                        deepcopy(state),
                        ghostLoc["W"].copy(),
                        move,
                        score.copy(),
                        deepcopy(ghostOnPellet),
                    )

                    evalMoveScores = minimax(
                        1,
                        k,
                        moveCounter,
                        tempState,
                        pacmanLoc.copy(),
                        tempAgent,
                        deepcopy(ghostOnPellet),
                        score.copy(),
                    )

                    if evalMoveScores < minevalMoveScore:
                        randomMove = move
                        minevalMoveScore = evalMoveScores

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
                
                randomMove = ""
                minevalMoveScore = math.inf
                for move in temp:
                    
                    tempAgent = ghostLoc.copy()
                    tempState, tempAgent["X"] = moveAgent(
                        deepcopy(state),
                        ghostLoc["X"].copy(),
                        move,
                        score.copy(),
                        deepcopy(ghostOnPellet),
                    )

                    evalMoveScores = minimax(
                        2,
                        k,
                        moveCounter,
                        tempState,
                        pacmanLoc.copy(),
                        tempAgent,
                        deepcopy(ghostOnPellet),
                        score.copy(),
                    )

                    if evalMoveScores < minevalMoveScore:
                        randomMove = move
                        minevalMoveScore = evalMoveScores

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
                randomMove = ""
                minevalMoveScore = math.inf
                for move in temp:
                    
                    tempAgent = ghostLoc.copy()
                    tempState, tempAgent["Y"] = moveAgent(
                        deepcopy(state),
                        ghostLoc["Y"].copy(),
                        move,
                        score.copy(),
                        deepcopy(ghostOnPellet),
                    )

                    evalMoveScores = minimax(
                        3,
                        k,
                        moveCounter,
                        tempState,
                        pacmanLoc.copy(),
                        tempAgent,
                        deepcopy(ghostOnPellet),
                        score.copy(),
                    )

                    if evalMoveScores < minevalMoveScore:
                        randomMove = move
                        minevalMoveScore = evalMoveScores

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
            # if (numberOfAgents == 5) and ((moveCounter-1)%numberOfAgents == 4):

            temp = validMoves(state, ghostLoc["Z"][0], ghostLoc["Z"][1])

            if temp:
                
                randomMove = ""
                minevalMoveScore = math.inf
                for move in temp:
                    
                    tempAgent = ghostLoc.copy()
                    tempState, tempAgent["Z"] = moveAgent(
                        deepcopy(state),
                        ghostLoc["Z"].copy(),
                        move,
                        score.copy(),
                        deepcopy(ghostOnPellet),
                    )

                    evalMoveScores = minimax(
                        1,
                        k,
                        moveCounter,
                        tempState,
                        pacmanLoc.copy(),
                        tempAgent,
                        deepcopy(ghostOnPellet),
                        score.copy(),
                    )

                    if evalMoveScores < minevalMoveScore:
                        randomMove = move
                        minevalMoveScore = evalMoveScores
                        
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
    problem_id = 5
    file_name_problem = str(test_case_id) + ".prob"
    file_name_sol = str(test_case_id) + ".sol"
    path = os.path.join("test_cases", "p" + str(problem_id))
    problem = parse.read_layout_problem(os.path.join(path, file_name_problem))
    k = int(sys.argv[2])
    num_trials = int(sys.argv[3])
    verbose = bool(int(sys.argv[4]))
    print("test_case_id:", test_case_id)
    print("k:", k)
    print("num_trials:", num_trials)
    print("verbose:", verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = min_max_mulitple_ghosts(copy.deepcopy(problem), k)
        if winner == "Pacman":
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count / num_trials * 100
    end = time.time()
    print("time: ", end - start)
    print("win %", win_p)
