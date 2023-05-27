import os, sys

def read_graph_search_problem(file_path):
    
    with open(file_path, 'r') as file:
        problem = file.read()
        
    problem = problem.split('\n')
    
    startState = problem[0].split()[-1]
    goalState = problem[1][-1]
    stateSpaceGraph = dict()
    heuristicDict = dict()
    
    for i in range(2,len(problem)):
        if (len(problem[i].split()))==3:
            break
        
        else:
            stateSpaceGraph[problem[i].split()[0]] = []
            heuristicDict[problem[i].split()[0]] = float(problem[i].split()[1])
    
    for el in problem[i:]:
        data = (float(el.split()[2]), el.split()[1])
        stateSpaceGraph[el.split()[0]].append(data)

    return [startState, goalState, stateSpaceGraph,heuristicDict]

def read_8queens_search_problem(file_path):
    
    with open(file_path, 'r') as file:
        problem = file.read()

    return [row.split() for row in problem.split('\n')]
    

if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        if int(problem_id) <= 5:
            problem = read_graph_search_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        else:
            problem = read_8queens_search_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')