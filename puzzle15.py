
import math

astar_result = []
bfs_result = []

def puzz_best_first(start,end):
    """
    Best First Search using breadth first search logic
    """
    front = [[puzzle]]
    expanded = []
    expanded_nodes=0
    while front:
        i = 0
        for j in range(1, len(front)):   
            if len(front[i]) > len(front[j]):
                i = j
        path = front[i]         
        front = front[:i] + front[i+1:]
        endnode = path[-1]
        if endnode in expanded: continue
        for k in moves(endnode):
            if k in expanded: continue
            front.append(path + [k])
        expanded.append(endnode)
        expanded_nodes += 1
        if endnode == end: break
    bfs_result.append(len(path))

def puzz_astar(start,end):
    """
    A* algorithm
    """
    count = 0
    # change the heuristic_1 value for ruuning for different heuristic
    front = [[heuristic_1(start), start]]
    expanded = []
    expanded_nodes=0
    while front:
        i = 0
        for j in range(1, len(front)):
            if front[i][0] > front[j][0]:
                i = j
        path = front[i]
        front = front[:i] + front[i+1:]
        endnode = path[-1]
        if endnode == end:
            break
        if endnode in expanded: continue
        for k in moves(endnode):
            if k in expanded: continue
            newpath = [path[0] + heuristic_1(k) - heuristic_1(endnode)] + path[1:] + [k] 
            front.append(newpath)
            expanded.append(endnode)
        expanded_nodes += 1 
    astar_result.append(len(path))

def moves(mat): 
    """
    Returns a list of all possible moves
    """
    output = []  
    m = eval(mat)   
    i = 0
    while 0 not in m[i]: 
        i += 1
    j = m[i].index(0); 

    if i > 0:                                   
      m[i][j], m[i-1][j] = m[i-1][j], m[i][j]; 
      output.append(str(m))
      m[i][j], m[i-1][j] = m[i-1][j], m[i][j]; 
      
    if i < 3:                                   
      m[i][j], m[i+1][j] = m[i+1][j], m[i][j]   
      output.append(str(m))
      m[i][j], m[i+1][j] = m[i+1][j], m[i][j]

    if j > 0:                                                      
      m[i][j], m[i][j-1] = m[i][j-1], m[i][j]  
      output.append(str(m))
      m[i][j], m[i][j-1] = m[i][j-1], m[i][j]

    if j < 3:                                   
      m[i][j], m[i][j+1] = m[i][j+1], m[i][j]  
      output.append(str(m))
      m[i][j], m[i][j+1] = m[i][j+1], m[i][j]

    return output

def heuristic_1(puzz):
    """
    Counts the number of misplaced tiles
    """ 
    misplaced = 0
    compare = 0
    m = eval(puzz)
    for i in range(4):
        for j in range(4):
            if m[i][j] != compare:
                misplaced += 1
            compare += 1
    return misplaced

def heuristic_2(puzz):
    """
    Manhattan distance
    """  
    distance = 0
    m = eval(puzz)          
    for i in range(4):
        for j in range(4):
            if m[i][j] == 0: 
                continue
            distance += abs(i - (m[i][j]/4)) + abs(j -  (m[i][j]%4))
    return distance

def heuristic_3(puzz):
    """
    Euclidean distance
    """  
    distance = 0
    m = eval(puzz)          
    for i in range(4):
        for j in range(4):
            if m[i][j] == 0: 
                continue
            distance += math.sqrt((i - (m[i][j]/4))**2 + (j -  (m[i][j]%4))**2)
    return distance

if __name__ == '__main__':

    puzzle = str([[1, 0, 2, 3],[4, 5, 6, 7], [8, 9, 10, 11],[12, 13, 14, 15]])
    end = str([[0, 1, 2, 3],[4, 5, 6, 7], [8, 9, 10, 11],[12, 13, 14, 15]])    
    puzz_astar(puzzle,end)
    puzz_best_first(puzzle,end)

    puzzle = str([[1, 2, 6, 3],[4, 9, 5, 7], [8, 13, 11, 15],[12, 14, 0, 10]])
    end = str([[0, 1, 2, 3],[4, 5, 6, 7], [8, 9, 10, 11],[12, 13, 14, 15]])
    puzz_astar(puzzle,end)
    puzz_best_first(puzzle,end)
    
    puzzle = str([[1, 2, 0, 3],[4, 5, 6, 7], [8, 9, 10, 11],[12, 13, 14, 15]])
    end = str([[0, 1, 2, 3],[4, 5, 6, 7], [8, 9, 10, 11],[12, 13, 14, 15]])    
    puzz_astar(puzzle,end)
    puzz_best_first(puzzle,end)

    puzzle = str([[1, 2, 3, 0],[4, 5, 6, 7], [8, 9, 10, 11],[12, 13, 14, 15]])
    end = str([[0, 1, 2, 3],[4, 5, 6, 7], [8, 9, 10, 11],[12, 13, 14, 15]])    
    puzz_astar(puzzle,end)
    puzz_best_first(puzzle,end)

    puzzle = str([[1, 0, 2, 3],[4, 5, 6, 7], [8, 9, 10, 11],[12, 13, 14, 15]])    
    end = str([[0, 1, 2, 3],[4, 5, 6, 7], [8, 9, 10, 11],[12, 13, 14, 15]])    
    puzz_astar(puzzle,end)
    puzz_best_first(puzzle,end)

    print("Average steps of A *")
    print(astar_result)
    print(sum(astar_result)/5.0)

    print("Average steps of BFS")
    print(bfs_result)
    print(sum(bfs_result)/5.0)
