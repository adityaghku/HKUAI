import sys, random, grader, parse

# I did not use classes, I am not familiar with OOP. I used mutable arrays
# to update everything

def deepcopy(array_2d):
    return [row[:] for row in array_2d]


def manhattanDistance(point1, point2):
    return abs(point2[0] - point1[0]) + abs(point2[1] - point1[1])

#returns position of all pellets
def allPellets(state):

    ans = []

    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == ".":
                ans.append([i, j])
    return ans

#for output
def printState(state):
    ans = ""

    for row in state:
        ans += "".join([str(x) for x in row])
        ans += "\n"

    return ans


def initialPacmanLoc(state):

    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == "P":
                return [i, j]


def initialGhostLoc(state):

    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == "W":
                return [i, j]


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


# Boolean to check if the ghost is on the pellet for printing and replacing
def noPellets(state, ghostOnPellet):
    for i in state:
        for j in i:
            if j == ".":
                return False

    if ghostOnPellet[0]:
        return False
    return True


# moves either ghost or pacman and returns the new agent loc and the new state
def moveAgent(state, agent, move, score, ghostOnPellet):

    agentCharacter = state[agent[0]][agent[1]]

    if agentCharacter == "P":

        if move == "W":
            if state[agent[0]][agent[1] - 1] == ".":
                score[0] += 10

            if state[agent[0]][agent[1] - 1] in ["W", "X", "Y", "Z"]:

                state[agent[0]][agent[1]] = " "
                agent[1] -= 1

                score[0] -= 500
                return state, agent

            state[agent[0]][agent[1] - 1] = agentCharacter
            state[agent[0]][agent[1]] = " "
            agent[1] -= 1

            return state, agent

        elif move == "N":

            if state[agent[0] - 1][agent[1]] == ".":
                score[0] += 10

            if state[agent[0] - 1][agent[1]] in ["W", "X", "Y", "Z"]:

                state[agent[0]][agent[1]] = " "

                agent[0] -= 1
                score[0] -= 500

                return state, agent

            state[agent[0] - 1][agent[1]] = agentCharacter
            state[agent[0]][agent[1]] = " "
            agent[0] -= 1

            return state, agent

        elif move == "S":

            if state[agent[0] + 1][agent[1]] == ".":
                score[0] += 10

            if state[agent[0] + 1][agent[1]] in ["W", "X", "Y", "Z"]:

                state[agent[0]][agent[1]] = " "

                agent[0] += 1
                score[0] -= 500

                return state, agent

            state[agent[0] + 1][agent[1]] = agentCharacter
            state[agent[0]][agent[1]] = " "
            agent[0] += 1

            return state, agent

        else:
            if state[agent[0]][agent[1] + 1] == ".":
                score[0] += 10

            if state[agent[0]][agent[1] + 1] in ["W", "X", "Y", "Z"]:

                state[agent[0]][agent[1]] = " "
                agent[1] += 1
                score[0] -= 500

                return state, agent

            state[agent[0]][agent[1] + 1] = agentCharacter
            state[agent[0]][agent[1]] = " "
            agent[1] += 1

            return state, agent

    else:
        if move == "W":
            if ghostOnPellet[0]:
                if state[agent[0]][agent[1] - 1] == ".":
                    ghostOnPellet[0] = True
                else:
                    ghostOnPellet[0] = False

                state[agent[0]][agent[1] - 1] = agentCharacter
                state[agent[0]][agent[1]] = "."
                agent[1] -= 1
                return state, agent

            if state[agent[0]][agent[1] - 1] == ".":
                ghostOnPellet[0] = True

            else:
                ghostOnPellet[0] = False

            if state[agent[0]][agent[1] - 1] == "P":
                score[0] -= 500

            state[agent[0]][agent[1] - 1] = agentCharacter
            state[agent[0]][agent[1]] = " "
            agent[1] -= 1
            return state, agent

        elif move == "N":

            if ghostOnPellet[0]:
                if state[agent[0] - 1][agent[1]] == ".":
                    ghostOnPellet[0] = True

                else:
                    ghostOnPellet[0] = False

                state[agent[0] - 1][agent[1]] = agentCharacter
                state[agent[0]][agent[1]] = "."
                agent[0] -= 1
                return state, agent

            if state[agent[0] - 1][agent[1]] == ".":
                ghostOnPellet[0] = True

            else:
                ghostOnPellet[0] = False

            if state[agent[0] - 1][agent[1]] == "P":
                score[0] -= 500

            state[agent[0] - 1][agent[1]] = agentCharacter
            state[agent[0]][agent[1]] = " "
            agent[0] -= 1

            return state, agent

        elif move == "S":

            if ghostOnPellet[0]:
                if state[agent[0] + 1][agent[1]] == ".":
                    ghostOnPellet[0] = True

                else:
                    ghostOnPellet[0] = False
                state[agent[0] + 1][agent[1]] = agentCharacter
                state[agent[0]][agent[1]] = "."
                agent[0] += 1
                return state, agent

            if state[agent[0] + 1][agent[1]] == ".":
                ghostOnPellet[0] = True

            else:
                ghostOnPellet[0] = False

            if state[agent[0] + 1][agent[1]] == "P":
                score[0] -= 500

            state[agent[0] + 1][agent[1]] = agentCharacter
            state[agent[0]][agent[1]] = " "
            agent[0] += 1

            return state, agent

        else:
            if ghostOnPellet[0]:
                if state[agent[0]][agent[1] + 1] == ".":
                    ghostOnPellet[0] = True

                else:
                    ghostOnPellet[0] = False

                state[agent[0]][agent[1] + 1] = agentCharacter
                state[agent[0]][agent[1]] = "."
                agent[1] += 1
                return state, agent

            if state[agent[0]][agent[1] + 1] == ".":
                ghostOnPellet[0] = True

            else:
                ghostOnPellet[0] = False

            if state[agent[0]][agent[1] + 1] == "P":
                score[0] -= 500

            state[agent[0]][agent[1] + 1] = agentCharacter
            state[agent[0]][agent[1]] = " "
            agent[1] += 1

            return state, agent

# Termination condition
def pacmanAlive(state):
    for i in state:
        for j in i:
            if j == "P":
                return True

    return False


def random_play_single_ghost(problem):

    seed, allMoves, state = problem
    random.seed(seed, version=1)

    pacmanLoc = initialPacmanLoc(state)
    ghostLoc = initialGhostLoc(state)

    moveCounter = 1

    score = [0]

    ghostOnPellet = [False]

    ans = ""
    ans += "seed: " + str(int(seed)) + "\n"
    ans += str(score[0]) + "\n"
    ans += printState(state)
    
    # While loop until end 
    while not noPellets(state, ghostOnPellet) and pacmanAlive(state):

        if moveCounter % 2 == 1: #Is it pacman or ghost
            
            randomMove = random.choice(validMoves(state, pacmanLoc[0], pacmanLoc[1]))

            ans += str(moveCounter) + ": P moving " + str(randomMove) + "\n"

            score[0] -= 1

            state, pacmanLoc = moveAgent(
                state, pacmanLoc, randomMove, score, ghostOnPellet
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

    else:
        ans += "WIN: Ghost"

    return ans


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(
        problem_id, test_case_id, random_play_single_ghost, parse.read_layout_problem
    )
