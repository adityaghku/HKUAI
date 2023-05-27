import sys, parse, grader
from p6 import number_of_attacks, copyArray, stringToArray

#Print function for 2d array
def arrayToString(problem):
    
    ans = ""
    for row in problem:
        ans+= " ".join([str(x) for x in row])
        ans+='\n'

    return ans[:-1]



#Main function
def better_board(problem):
    
    boardCost = stringToArray(number_of_attacks(problem))
    
    checkArray = copyArray(boardCost)
    
    for i in range(8):
        for j in range(8):
            boardCost[i][j] = int(boardCost[i][j])
            checkArray[i][j] = int(checkArray[i][j])
            
            if problem[i][j] == 'q':
                boardCost[i][j] = 200
    
    attacks = 64
    x = 0 
    y = 0
    
    #Minimum of non-queen values
    for j in range(8):
        for i in range(8):
            if boardCost[i][j] < attacks:
                attacks = boardCost[i][j]
                x, y = i, j
    
    updatedBoard = copyArray(problem)
    
    # To check if moving the queen won't reduce the cost
    for i in range(8):
        
        if problem[i][y] == 'q':
            movedQueen = i
        
        updatedBoard[i][y] = '.'
        
    updatedBoard[x][y] = 'q'
    
    comparisonArray = stringToArray(number_of_attacks(updatedBoard))
    
    for i in range(8):
        for j in range(8):
            comparisonArray[i][j] = int(comparisonArray[i][j])

    #No need to move the queen
    if checkArray[movedQueen][y] == comparisonArray[x][y]:
        return arrayToString(problem)
    
    else:
        return arrayToString(updatedBoard)


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 7
    grader.grade(problem_id, test_case_id, better_board, parse.read_8queens_search_problem)