import sys, grader, parse, collections

def dfs_search(problem):

    startState = problem[0]
    goalState = problem[1]
    stateSpaceGraph = problem[2]

    
    frontier = collections.deque([startState])
    exploredSet = set()
    
    exploredOrder = []
    solution = []
    
    while(frontier):
        
        node = frontier.pop()
        
        if (node.endswith(goalState)):
            solution.append(node)
            return " ".join(exploredOrder) + "\n" + " ".join(solution)
            
            
        current = node.split()[-1]
        
        if current not in exploredSet:
            
            exploredOrder.append(current)
            exploredSet.add(current)
            
            for child in stateSpaceGraph[current]:
                
                if child[1] != current:
                    frontier.append(node + ' ' + child[1])
    

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, dfs_search, parse.read_graph_search_problem)