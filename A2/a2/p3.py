import sys, grader, parse, math, random

from p1 import printState, initialPacmanLoc, pacmanAlive, moveAgent

# updated to deal with multiple ghosts
def noPellets(state, ghostOnPellet):

    for i in state:
        for j in i:
            if j == ".":
                return False

    for x in ghostOnPellet:
        if x[0] == True:
            return False

    return True

# dict with 'W':[] to get locs
def initialGhostLocs(state):

    ghostLocs = dict()

    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] in ["W", "X", "Y", "Z"]:
                ghostLocs[state[i][j]] = [i, j]

    return ghostLocs

#same as before but updated for multi ghost case
def validMoves(state, agentLoci, agentLocj):

    moves = []

    if state[agentLoci][agentLocj] == "P":
        if state[agentLoci][agentLocj + 1] not in ["%"]:
            moves.append("E")

        if state[agentLoci - 1][agentLocj] not in ["%"]:
            moves.append("N")

        if state[agentLoci + 1][agentLocj] not in ["%"]:
            moves.append("S")

        if state[agentLoci][agentLocj - 1] not in ["%"]:
            moves.append("W")

    else:
        if state[agentLoci][agentLocj + 1] not in ["W", "X", "Y", "Z", "%"]:
            moves.append("E")

        if state[agentLoci - 1][agentLocj] not in ["W", "X", "Y", "Z", "%"]:
            moves.append("N")

        if state[agentLoci + 1][agentLocj] not in ["W", "X", "Y", "Z", "%"]:
            moves.append("S")

        if state[agentLoci][agentLocj - 1] not in ["W", "X", "Y", "Z", "%"]:
            moves.append("W")

    return moves


def random_play_multiple_ghosts(problem):

    seed, allMoves, state = problem
    random.seed(seed, version=1)

    pacmanLoc = initialPacmanLoc(state)
    ghostLoc = initialGhostLocs(state)
    
    #the move counter now loops from 0 to numberOfAgents instead of just 0 and 1
    numberOfAgents = len(ghostLoc) + 1
    
    #2d array which gets updated for each ghost same as in p1.py
    ghostOnPellet = []
    for i in range(numberOfAgents - 1):
        ghostOnPellet.append([False])

    moveCounter = 1

    score = [0]

    ans = ""
    ans += "seed: " + str(int(seed)) + "\n"
    ans += str(score[0]) + "\n"
    ans += printState(state)
    
    #no difference from p1.py except multiple ghosts so we have more if statements

    while not noPellets(state, ghostOnPellet) and pacmanAlive(state):

        if (moveCounter - 1) % numberOfAgents == 0:

            randomMove = random.choice(validMoves(state, pacmanLoc[0], pacmanLoc[1]))

            ans += str(moveCounter) + ": P moving " + str(randomMove) + "\n"

            score[0] -= 1

            state, pacmanLoc = moveAgent(state, pacmanLoc, randomMove, score, None)

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
            # if (numberOfAgents == 5) and ((moveCounter-1)%numberOfAgents == 4):

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

    else:
        ans += "WIN: Ghost"

    return ans


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 3
    grader.grade(
        problem_id, test_case_id, random_play_multiple_ghosts, parse.read_layout_problem
    )
