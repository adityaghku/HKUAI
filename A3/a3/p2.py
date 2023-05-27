import sys, grader, parse

from p1 import deepcopy


def movePlayerP2(grid, move, playerPos):

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


def initialiseVGrid(grid):
    temp = []
    for i in range(len(grid)):
        temp2 = []
        for j in range(len(grid[1])):
            if grid[i][j] == "#":
                temp2.append("#####")
            else:
                temp2.append(0.0)
        temp.append(temp2)
    return temp


def outputVGrid(policy):
    temp = ""

    for i in range(len(policy)):
        for j in range(len(policy[i])):
            if policy[i][j] == "#####":
                temp += "|{:^7}|".format(policy[i][j])
            else:
                temp += "|{:7.2f}|".format(policy[i][j])
        temp += "\n"

    return temp


def policy_evaluation(problem):

    discount, noise, livingReward, iterations, grid, policy = problem
    noise = float(noise)
    discount = float(discount)

    d = {
        "N": ["N", "E", "W"],
        "E": ["E", "S", "N"],
        "S": ["S", "W", "E"],
        "W": ["W", "N", "S"],
    }

    vGrid = initialiseVGrid(grid)

    vGridArray = [deepcopy(vGrid)]

    k = 0
    ans = "V^pi_k=" + str(k) + "\n"
    ans += outputVGrid(vGrid)

    for i in range(len(policy)):
        for j in range(len(policy[i])):
            if policy[i][j] == "exit":
                vGrid[i][j] = float(grid[i][j])
            else:
                vGrid[i][j] += livingReward

    k += 1
    ans += "V^pi_k=" + str(k) + "\n"
    ans += outputVGrid(vGrid)

    while k < iterations - 1:
        vGridArray.append(deepcopy(vGrid))

        for i in range(len(policy)):
            for j in range(len(policy[i])):

                tempVValue = 0
                intendedMove = policy[i][j]

                if intendedMove not in ["#", "exit"]:
                    for move in d[intendedMove]:

                        if move == intendedMove:
                            _, newPos, _ = movePlayerP2(
                                deepcopy(grid), move, [i, j].copy()
                            )

                            if grid[newPos[0]][newPos[1]] in ["_", "S"]:

                                tempVValue += (1 - noise * 2) * (
                                    0 + vGridArray[-1][newPos[0]][newPos[1]]
                                )

                            else:
                                tempVValue += (1 - noise * 2) * (
                                    float(grid[newPos[0]][newPos[1]]) + 0
                                )

                        else:
                            _, newPos, _ = movePlayerP2(
                                deepcopy(grid), move, [i, j].copy()
                            )

                            if grid[newPos[0]][newPos[1]] in ["_", "S"]:
                                tempVValue += noise * (
                                    0 + vGridArray[-1][newPos[0]][newPos[1]]
                                )
                            else:
                                tempVValue += noise * (
                                    float(grid[newPos[0]][newPos[1]]) + 0
                                )

                    vGrid[i][j] = discount * tempVValue
                    vGrid[i][j] += livingReward

        k += 1
        ans += "V^pi_k=" + str(k) + "\n"
        ans += outputVGrid(vGrid)

    return ans.removesuffix("\n")


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    # test_case_id = -7
    problem_id = 2
    grader.grade(
        problem_id,
        test_case_id,
        policy_evaluation,
        parse.read_grid_mdp_problem_p2,
    )
