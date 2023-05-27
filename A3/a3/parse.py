def read_grid_mdp_problem_p1(file_path):

    with open(file_path, "r") as file:
        problem = file.read()

    seed = float(problem.split()[1])
    noise = float(problem.split()[3])
    livingReward = float(problem.split()[5])

    problem = problem.split("\n")

    tempgrid = problem[3 + 1 : problem.index("policy:")]
    temppolicy = problem[problem.index("policy:") + 1 :]

    grid = []
    for i in range(len(tempgrid)):
        temp = []
        for j in tempgrid[i].split():
            if j != " ":
                temp.append(j)
        grid.append(temp)

    policy = []
    for i in range(len(temppolicy)):
        temp = []
        for j in temppolicy[i].split():
            if j != " ":
                temp.append(j)
        policy.append(temp)

    return seed, noise, livingReward, grid, policy


def read_grid_mdp_problem_p2(file_path):

    with open(file_path, "r") as file:
        problem = file.read()

    discount = float(problem.split()[1])
    noise = float(problem.split()[3])
    livingReward = float(problem.split()[5])
    iterations = float(problem.split()[7])

    problem = problem.split("\n")

    tempgrid = problem[4 + 1 : problem.index("policy:")]
    temppolicy = problem[problem.index("policy:") + 1 :]

    grid = []
    for i in range(len(tempgrid)):
        temp = []
        for j in tempgrid[i].split():
            if j != " ":
                temp.append(j)
        grid.append(temp)

    policy = []
    for i in range(len(temppolicy)):
        temp = []
        for j in temppolicy[i].split():
            if j != " ":
                temp.append(j)
        policy.append(temp)

    return discount, noise, livingReward, iterations, grid, policy


def read_grid_mdp_problem_p3(file_path):

    with open(file_path, "r") as file:
        problem = file.read()

    discount = float(problem.split()[1])
    noise = float(problem.split()[3])
    livingReward = float(problem.split()[5])
    iterations = float(problem.split()[7])

    problem = problem.split("\n")

    tempgrid = problem[4 + 1 :]

    grid = []
    for i in range(len(tempgrid)):
        temp = []
        for j in tempgrid[i].split():
            if j != " ":
                temp.append(j)
        grid.append(temp)

    return discount, noise, livingReward, iterations, grid
