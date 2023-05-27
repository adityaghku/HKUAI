import sys, parse, grader
from heapq import heappush, heappop

def ucs_search(problem):

    startState = problem[0]
    goalState = problem[1]
    stateSpaceGraph = problem[2]
    
    frontier = []
    heappush(frontier, (0, startState))

    exploredSet = set()
    
    exploredOrder = []
    solution = []
    
    while(frontier):
        
        node = heappop(frontier)
        
        
        if (node[1].endswith(goalState)):
            solution.append(node[1])
            return " ".join(exploredOrder) + "\n" + " ".join(solution)
            
        current = node[1].split()[-1]
        
        if current not in exploredSet:
            
            exploredOrder.append(current)
            exploredSet.add(current)
            
            for child in stateSpaceGraph[current]:
                heappush(frontier, (node[0]+child[0], node[1]+ ' ' +child[1]))


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 3
    grader.grade(problem_id, test_case_id, ucs_search, parse.read_graph_search_problem)
    
