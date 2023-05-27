import sys, grader, parse, random

# from collections import Counter


# Needs to be changed
def outputNum(x):
    if int(str(round(x, 7)).split(".")[1]) == 0:
        return str(x).split(".")[0] + ".0"

    return "{:g}".format(x)


def deepcopy(array_2d):
    return [row[:] for row in array_2d]


def movePlayer(grid, move, playerPos):

    if move == "exit":
        return (
            fixedInitialGrid,
            None,
            float(fixedInitialGrid[playerPos[0]][playerPos[1]]),
        )

    if move == "N":
        if (playerPos[0] - 1 < 0) or (grid[playerPos[0] - 1][playerPos[1]] == "#"):
            return grid, playerPos, 0

        if playerPos == fixedStartLoc:
            grid[playerPos[0]][playerPos[1]] = "S"

            grid[playerPos[0] - 1][playerPos[1]] = "P"
            playerPos[0] -= 1
            return grid, playerPos, 0

        else:
            grid[playerPos[0]][playerPos[1]] = "_"

            grid[playerPos[0] - 1][playerPos[1]] = "P"
            playerPos[0] -= 1

            return grid, playerPos, 0

    if move == "S":
        if playerPos[0] + 1 >= columnLength or (
            grid[playerPos[0] + 1][playerPos[1]] == "#"
        ):
            return grid, playerPos, 0

        if playerPos == fixedStartLoc:
            grid[playerPos[0]][playerPos[1]] = "S"

            grid[playerPos[0] + 1][playerPos[1]] = "P"
            playerPos[0] += 1
            return grid, playerPos, 0

        else:
            grid[playerPos[0]][playerPos[1]] = "_"

            grid[playerPos[0] + 1][playerPos[1]] = "P"
            playerPos[0] += 1
            return grid, playerPos, 0

    if move == "W":
        if playerPos[1] - 1 < 0 or (grid[playerPos[0]][playerPos[1] - 1] == "#"):
            return grid, playerPos, 0

        if playerPos == fixedStartLoc:
            grid[playerPos[0]][playerPos[1]] = "S"

            grid[playerPos[0]][playerPos[1] - 1] = "P"
            playerPos[1] -= 1
            return grid, playerPos, 0

        else:
            grid[playerPos[0]][playerPos[1]] = "_"

            grid[playerPos[0]][playerPos[1] - 1] = "P"
            playerPos[1] -= 1
            return grid, playerPos, 0

    if move == "E":
        if playerPos[1] + 1 >= rowLength or (
            grid[playerPos[0]][playerPos[1] + 1] == "#"
        ):
            return grid, playerPos, 0

        if playerPos == fixedStartLoc:
            grid[playerPos[0]][playerPos[1]] = "S"

            grid[playerPos[0]][playerPos[1] + 1] = "P"
            playerPos[1] += 1
            return grid, playerPos, 0
        else:
            grid[playerPos[0]][playerPos[1]] = "_"

            grid[playerPos[0]][playerPos[1] + 1] = "P"
            playerPos[1] += 1
            return grid, playerPos, 0

    return None, None, None  # debugging failsafe


def startLoc(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "S":
                return [i, j]


def outputGrid(grid):
    temp = ""

    for i in grid:
        frmt = "{:>5}" * len(i)
        temp += frmt.format(*i)
        temp += "\n"

    return temp


def play_episode(problem):

    seed, noise, livingReward, grid, policy = problem

    if seed != -1:
        random.seed(seed, version=1)

    d = {
        "N": ["N", "E", "W"],
        "E": ["E", "S", "N"],
        "S": ["S", "W", "E"],
        "W": ["W", "N", "S"],
    }

    global fixedInitialGrid
    fixedInitialGrid = deepcopy(grid)

    global rowLength
    rowLength = len(grid[0])

    global columnLength
    columnLength = len(grid)

    global fixedStartLoc
    fixedStartLoc = startLoc(grid)
    playerPos = fixedStartLoc.copy()

    stillPlaying = True
    cumReward = 0.0

    grid[playerPos[0]][playerPos[1]] = "P"

    ans = "Start state:\n"
    ans += outputGrid(grid)

    ans += "Cumulative reward sum: " + str(cumReward) + "\n"
    ans += "-------------------------------------------- \n"

    while stillPlaying:
        intendedMove = policy[playerPos[0]][playerPos[1]]

        if intendedMove == "exit":
            move = "exit"

        else:
            move = random.choices(
                population=d[intendedMove], weights=[1 - noise * 2, noise, noise]
            )[0]

        receivedReward = 0
        grid, playerPos, receivedReward = movePlayer(grid, move, playerPos)

        if move != "exit":
            receivedReward += livingReward
        cumReward += receivedReward

        ans += "Taking action: " + move + " (intended: " + intendedMove + ")\n"

        ans += "Reward received: " + outputNum(receivedReward) + "\n"

        ans += "New state:\n"
        ans += outputGrid(grid)

        ans += "Cumulative reward sum: " + outputNum(cumReward) + "\n"
        ans += "-------------------------------------------- \n"

        if move == "exit":
            stillPlaying = False

    return ans.removesuffix("\n-------------------------------------------- \n")


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    # test_case_id = 1
    problem_id = 1
    grader.grade(problem_id, test_case_id, play_episode, parse.read_grid_mdp_problem_p1)
