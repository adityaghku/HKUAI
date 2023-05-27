import sys, grader, parse, math

from p1 import deepcopy
from p2 import outputVGrid, initialiseVGrid


def movePlayerP3(grid, move, playerPos):

    if move == "exit":
        return grid, None, float(grid[playerPos[0]][playerPos[1]])

    if move == "N":
        if (playerPos[0] - 1 < 0) or (
            grid[playerPos[0] - 1][playerPos[1]] == "#"
        ):
            return grid, playerPos, 0

        grid[playerPos[0]][playerPos[1]] = "_"

        grid[playerPos[0] - 1][playerPos[1]] = "P"
        playerPos[0] -= 1

        return grid, playerPos, 0

    if move == "S":
        if playerPos[0] + 1 >= len(grid) or (
            grid[playerPos[0] + 1][playerPos[1]] == "#"
        ):
            return grid, playerPos, 0

        grid[playerPos[0]][playerPos[1]] = "_"

        grid[playerPos[0] + 1][playerPos[1]] = "P"
        playerPos[0] += 1
        return grid, playerPos, 0

    if move == "W":
        if playerPos[1] - 1 < 0 or (
            grid[playerPos[0]][playerPos[1] - 1] == "#"
        ):
            return grid, playerPos, 0

        grid[playerPos[0]][playerPos[1]] = "_"

        grid[playerPos[0]][playerPos[1] - 1] = "P"
        playerPos[1] -= 1
        return grid, playerPos, 0

    if move == "E":
        if playerPos[1] + 1 >= len(grid[0]) or (
            grid[playerPos[0]][playerPos[1] + 1] == "#"
        ):
            return grid, playerPos, 0

        grid[playerPos[0]][playerPos[1]] = "_"

        grid[playerPos[0]][playerPos[1] + 1] = "P"
        playerPos[1] += 1
        return grid, playerPos, 0

    return None, None, None  # debugging failsafe


def outputPolicy(policy):
    temp = ""

    for i in range(len(policy)):
        for j in range(len(policy[i])):
            temp += "|{:^3}|".format(policy[i][j])
        temp += "\n"

    return temp


def initialisePolicy(grid):
    temp = []
    for i in range(len(grid)):
        temp2 = []
        for j in range(len(grid[i])):
            if grid[i][j] == "#":
                temp2.append("#")
            elif grid[i][j] in ["_", "S"]:
                temp2.append("N")
            else:
                temp2.append("x")
        temp.append(temp2)
    return temp


def value_iteration(problem):
    global noise, discount, livingReward, d, moves

    discount, noise, livingReward, iterations, grid = problem
    noise = float(noise)
    discount = float(discount)
    livingReward = float(livingReward)

    d = {
        "N": ["N", "E", "W"],
        "E": ["E", "S", "N"],
        "S": ["S", "W", "E"],
        "W": ["W", "N", "S"],
    }

    moves = ["N", "E", "S", "W"]

    vGrid = initialiseVGrid(grid)
    vGridArray = [deepcopy(vGrid)]

    k = 0
    ans = "V_k=" + str(k) + "\n"
    ans += outputVGrid(vGrid)

    policy = initialisePolicy(grid)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] not in ["#"]:
                if grid[i][j] not in ["_", "S"]:
                    vGrid[i][j] = float(grid[i][j])
                else:
                    vGrid[i][j] += livingReward

    k += 1
    ans += "V_k=" + str(k) + "\n"
    ans += outputVGrid(vGrid)
    ans += "pi_k=" + str(k) + "\n"
    ans += outputPolicy(policy)

    while k < iterations - 1:

        vGridArray.append(deepcopy(vGrid))

        for i in range(len(policy)):
            for j in range(len(policy[i])):
                if grid[i][j] not in ["_", "S", "#"]:
                    vGrid[i][j] = float(grid[i][j])

                else:
                    if policy[i][j] not in ["#"]:
                        maxScore = -math.inf

                        maxMove = ""
                        for move in moves:

                            tempScore = VScore(
                                grid,
                                move,
                                i,
                                j,
                                deepcopy(vGrid),
                                deepcopy(vGridArray[-1]),
                            )
                            # deal with rounding error
                            if tempScore > maxScore and (
                                abs(tempScore - maxScore) > 1e-5
                            ):
                                maxScore = tempScore
                                maxMove = move

                        vGrid[i][j] = maxScore

                        if grid[i][j] in ["_", "S"]:
                            policy[i][j] = maxMove

        k += 1
        ans += "V_k=" + str(k) + "\n"
        ans += outputVGrid(vGrid)
        ans += "pi_k=" + str(k) + "\n"
        ans += outputPolicy(policy)

    return ans[:-1]


def VScore(grid, intendedMove, i, j, vGrid, vGridArray):

    tempVValue = 0

    for move in d[intendedMove]:

        if move == intendedMove:
            _, newPos, _ = movePlayerP3(deepcopy(grid), move, [i, j].copy())

            if grid[newPos[0]][newPos[1]] in ["_", "S"]:

                tempVValue += (1 - noise * 2) * (
                    0 + vGridArray[newPos[0]][newPos[1]]
                )

            else:
                tempVValue += (1 - noise * 2) * (
                    float(grid[newPos[0]][newPos[1]]) + 0
                )

        else:
            _, newPos, _ = movePlayerP3(deepcopy(grid), move, [i, j].copy())

            if grid[newPos[0]][newPos[1]] in ["_", "S"]:
                tempVValue += noise * (0 + vGridArray[newPos[0]][newPos[1]])
            else:
                tempVValue += noise * (float(grid[newPos[0]][newPos[1]]) + 0)

    return (discount * tempVValue) + livingReward


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    # test_case_id = -4
    problem_id = 3
    grader.grade(
        problem_id,
        test_case_id,
        value_iteration,
        parse.read_grid_mdp_problem_p3,
    )
