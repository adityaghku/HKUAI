import sys, parse, grader  

#For cleaner syntax to convert a 8*8 string to arrray
def stringToArray(x):
    return [row.split() for row in x.split('\n')]

# output format for p6
def arrayToString2(x):
    return '\n'.join([' '.join(['{:2}'.format(item) for item in row]) for row in x])

# computes the number of queens attacking one cell
def attacksForOneCell(problem):

    def diagonal(queensLoc, q_1, q_2):
        rowDiff = abs(queensLoc[q_1][0] - queensLoc[q_2][0])
        colDiff = abs(queensLoc[q_1][1] - queensLoc[q_2][1])
        return rowDiff == colDiff

    numAttacks = 0
    queensLoc = [
        (i, j) for j in range(8)
        for i in range(8)
        if problem[i][j]
    ]


    for i in range(8):
        for j in range(i+1, 8):
            if queensLoc[i][0] == queensLoc[j][0]:
                numAttacks += 1
                continue

            if diagonal(queensLoc, i, j):
                numAttacks += 1 

    return numAttacks

#Returns a copy without reference to the 2d arrays
def copyArray(x):
    
    temp = []
    
    for i in range(8):
        temp1 = []
        for j in range(8):
            temp1.append(x[i][j])
        temp.append(temp1)
    
    return temp

#main function which returns the cost board
def number_of_attacks(problem):

    board = []
    
    #Converting board to boolean for convenience
    for i in range(8):
        temp = []
        for j in range(8):
            if problem[i][j] == 'q':
                temp.append(1)
            else:
                temp.append(0)
        board.append(temp)
    
    
    costBoard = [[200 for i in range(8)] for j in range(8)]
    
    for r in range(0,8):
        for c in range(0,8):
            if board[r][c] == 1:
                for r2 in range(8):
                    temp = copyArray(board)

                    temp[r][c] = 0
                    temp[r2][c] = 1
                    costBoard[r2][c] = attacksForOneCell(temp)
    
    
    return arrayToString2(costBoard)


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 6
    grader.grade(problem_id, test_case_id, number_of_attacks, parse.read_8queens_search_problem)