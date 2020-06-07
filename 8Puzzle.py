import random
import math

maximum_moves = 10000
goalState = [[1,2,3],
            [4,5,6],
            [7,8,0]]

final_Output = [[0,0,0],[0,0,0]]

def index(i,seq):
    if(len(seq) > 0):
        ind = -1
        for x in range(len(seq)):
            if(i == seq[x].cloned_matrix):
                ind = x
        return ind
    else:
        return -1

class EightPuzzle:

    def __init__(self):
        self.parentNode = None
        self.heuristicFValue = 0
        self.depth = 0
        self.cloned_matrix = []
        #self.no_of_Heuri_Functions = 3
        for i in range(3):
            self.cloned_matrix.append(goalState[i][:])

    def init_Matrix(self, values):
        i = 0
        for row in range(3):
            for col in range(3):
                self.cloned_matrix[row][col] = int(values[i])
                i = i+1

        self.initial_matrix = self.cloned_matrix
    def solution_path(self, path):
        if(self.parentNode == None):
            return path
        else:
            path.append(self)
            return self.parentNode.solution_path(path)

    def diff_moves(self):
        row,col = self.find(0)
        possible_matrix_move = []

        if(row > 0):
            possible_matrix_move.append((row-1,col))
        if(col > 0):
            possible_matrix_move.append((row, col-1))
        if(row < 2):
            possible_matrix_move.append((row+1, col))
        if(col < 2):
            possible_matrix_move.append((row, col+1))

        return possible_matrix_move
    
    def setValue(self, row, col,value):
        self.cloned_matrix[row][col] = value
    
    def getValue(self, row, col):
        return self.cloned_matrix[row][col]

    def swap(self, position_a, position_b):
        temp = self.getValue(*position_a)
        self.setValue(position_a[0],position_a[1],self.getValue(*position_b))
        self.setValue(position_b[0],position_b[1],temp)
    
    def cloneMatrix(self):
        p = EightPuzzle()
        for i in range(3):
            p.cloned_matrix[i] = self.cloned_matrix[i][:]
        return p

    def find(self,value):
        if(value < 0 or value > 8):
            raise Exception("value is out of range")

        for row in range(3):
            for col in range(3):
                if self.cloned_matrix[row][col] == value:
                    return row, col

    def possible_next_optSolution(self):
        possible_matrix_move = self.diff_moves()
        zero = self.find(0)

        def swap_and_clone(x, y):
            p = self.cloneMatrix()
            p.swap(x,y)
            p.depth = self.depth + 1
            p.parentNode = self
            return p
        return map(lambda  pair: swap_and_clone(zero,pair), possible_matrix_move)

    def A_star_Search(self, heuristicFunction):
        def isSolved(puzzle):
            return puzzle.cloned_matrix == goalState
        
        input_Matrix_List = [self]
        intermediate_Matrix_List = []
        move_count = 0

        while len(input_Matrix_List) > 0:
            x = input_Matrix_List.pop(0)
            move_count += 1
            herrustic_val = heuristicFunction(x)
            x.heuristicFValue = herrustic_val

            if(move_count > maximum_moves):
                print("max count reached, you didnt get the solution")
                return [], move_count
            
            if(isSolved(x)):
                if len(intermediate_Matrix_List) > 0:
                    return x.solution_path([]), move_count
                else:
                    return [x]
            
            next_possible_position = x.possible_next_optSolution()
            idOpen = idClose = -1
            for move in next_possible_position:
                idOpen = index(move.cloned_matrix, input_Matrix_List)
                idClose = index(move.cloned_matrix, intermediate_Matrix_List)
                herrustic_val = heuristicFunction(move)
                fval = herrustic_val + move.depth

                if(idClose == -1 and idOpen == -1):
                    move.heuristicFValue = herrustic_val
                    input_Matrix_List.append(move)
                elif idOpen > -1:
                    copy = input_Matrix_List[idOpen]
                    if fval < copy.heuristicFValue + copy.depth:
                        copy.heuristicFValue = herrustic_val
                        copy.parentNode = move.parentNode
                        copy.depth = move.depth
                elif idClose > -1:
                    copy = intermediate_Matrix_List[idClose]
                    if fval < copy.heuristicFValue + copy.depth:
                        move.heuristicFValue = herrustic_val
                        intermediate_Matrix_List.remove(copy)
                        input_Matrix_List.append(move)

            intermediate_Matrix_List.append(x)
            input_Matrix_List = sorted(input_Matrix_List, key=lambda p:p.heuristicFValue + p.depth)
        return [],move_count

    def best_First_Search(self, heuristicFunction):
        def isSolved(puzzle):
            return puzzle.cloned_matrix == goalState
        
        input_Matrix_List = [self]
        intermediate_Matrix_List = []
        move_count = 0
        while len(input_Matrix_List) > 0:
            x = input_Matrix_List.pop(0)
            move_count += 1

            if(move_count > maximum_moves):
                print("max count reached, you didnt get the solution")
                return [], move_count

            if(isSolved(x)):
                if(len(intermediate_Matrix_List) > 0):
                    return x.solution_path([]), move_count
                else:
                    return[x]
            
            next_possible_position = x.possible_next_optSolution()
            idOpen = idClose = -1
            for move in next_possible_position:
                idOpen = index(move.cloned_matrix, input_Matrix_List)
                idClose = index(move.cloned_matrix, intermediate_Matrix_List)
                herrustic_val = heuristicFunction(move)
                fval = herrustic_val

                if(idClose == -1 and idOpen == -1):
                    move.heuristicFValue = herrustic_val
                    input_Matrix_List.append(move)
                elif(idOpen > -1):
                    copy = input_Matrix_List[idOpen]
                    if(fval < copy.heuristicFValue):
                        copy.heuristicFValue = herrustic_val
                        copy.parentNode = move.parentNode
                        copy.depth = move.depth
                elif(idClose > -1):
                    copy = intermediate_Matrix_List[idClose]
                    if(fval < copy.heuristicFValue):
                        move.heuristicFValue = herrustic_val
                        intermediate_Matrix_List.remove(copy)
                        input_Matrix_List.append(move)
            intermediate_Matrix_List.append(x)
            input_Matrix_List = sorted(input_Matrix_List, key=lambda p: p.heuristicFValue)
        return [],move_count

def heuristic(puzzle,item_total_calc, total_calc):
    t = 0
    for row in range(3):
        for col in range(3):
            val = puzzle.getValue(row,col)
            if(val != 0):
                target_col = (val-1) % 3
                target_row = (val-1) / 3

                if target_row < 0:
                    target_row = 2
                t += item_total_calc(row,target_row,col,target_col)
    return total_calc(t)

def h_manhatten_distance(puzzle):
    return heuristic(puzzle,
                    lambda r,tr, c, tc: abs(tr-r) + abs(tc -c),
                    lambda t : t)

def h_euclidean_distance(puzzle):
    return heuristic(puzzle,
                    lambda r,tr,c,tc: math.sqrt((tr-r)**2 + (tc-c)**2),
                    lambda t:t)

def h_misplaced_tiles(puzzle):
    return heuristic(puzzle,
                    lambda r,tr,c,tc: missed_tiles_count(puzzle),
                    lambda t:t)

def missed_tiles_count(puzzle):
    count = 0
    for row in range(3):
        for col in range(3):
            if(puzzle.getValue(row,col) != goalState[row][col]):
                count = count + 1
    return count


def search(p):
    print("\n\n A* Manhattan distance")
    print("Initial state is : ",p.initial_matrix)
    path, count = p.A_star_Search(h_manhatten_distance)
    if(path != []):
        path.reverse()
        for i in path:
            print(i.cloned_matrix)
            final_Output[1][0] = final_Output[1][0] + len(path)
        print("A* and Manhattan distance in ", len(path) ,"steps exploring", count, "states")
    else:
        print("search aborted after exploring", count-1, "states")

    print("\n\n A* with Euclidean distance")
    print("Initial state is : ",p.initial_matrix)
    path, count = p.A_star_Search(h_euclidean_distance)
    if(path != []):
        path.reverse()
        for i in path:
            print(i.cloned_matrix)
            final_Output[1][1] = final_Output[1][1] + len(path)
        print("A* and Euclidean distance in", len(path), "steps exploring", count, "states")
    else:
        print("search aborted after exploring", count-1, "states")

    print("\n\n A* with Misplaced tiles")
    print("Initial state is : ",p.initial_matrix)
    path, count = p.A_star_Search(h_misplaced_tiles)
    if(path != []):
        path.reverse()
        for i in path:
            print(i.cloned_matrix)
            final_Output[1][2] = final_Output[1][2] + len(path)
        print("Solved with A* & Misplaced tiles in ", len(path) ,"steps exploring", count, "states")
    else:
        print("Search aborted after exploring", count-1, "states")

    print("\n\n BFS with Manhattan distance")
    print("Initial state is : ",p.initial_matrix)
    path, count = p.best_First_Search(h_manhatten_distance)
    if(path != []):
        path.reverse()
        for i in path:
            print(i.cloned_matrix)
            final_Output[0][0] = final_Output[0][0] +  len(path)
        print("Solved with BFS with Manhattan distance in ", len(path) ,"steps exploring", count, "states")
    else:
        print("Search aborted after exploring", count-1, "states")

    print("\n\n BFS with Euclidean distance")
    print("Initial state is : ",p.initial_matrix)
    path, count = p.best_First_Search(h_euclidean_distance)
    if(path != []):
        path.reverse()
        for i in path:
            print(i.cloned_matrix)
            final_Output[0][1] = final_Output[0][1] + len(path)
        print("Solved with BFS with Euclidean distance in ", len(path) ,"steps exploring", count, "states")
    else:
        print("Search aborted after exploring", count-1, "states")

    print("\n\nBFS with Misplaced tiles")
    print("Initial state is : ", p.initial_matrix)
    path, count = p.best_First_Search(h_misplaced_tiles)
    if(path != []):
        path.reverse()
        for i in path:
            print(i.cloned_matrix)
            final_Output[0][2] = final_Output[0][2] + len(path)
        print("Solved with BFS & Misplaced tiles in ", len(path) ,"steps exploring", count, "states")
    else:
        print("Search aborted after exploring", count-1, "states")

def main():
    #input_matrix = input('Enter your 8 puzzle string: ')
    p = EightPuzzle()
    p.init_Matrix('123450678')
    search(p)
    
    print( "*******************************************")
    #Functions to get all the data and average step count
    #print( "below are the given inputs for calculating average: " )
    p.init_Matrix('123405678')
    search(p)

    print( "*******************************************")

    p.init_Matrix('123456078')
    search(p)

    print( "*******************************************")

    p.init_Matrix('123045678')
    search(p)

    print( "*******************************************")

    p.init_Matrix('012345678')
    search(p)

    #print "*******************************************"

    print("Average Count")
    print( "A* & Manhattan distance: ",  final_Output[1][0]/5)
    print("A* & Euclidean distance: ", final_Output[1][1]/5)
    print("A* & Misplaced tiles: ",     final_Output[1][2]/5)
    print("BFS & Manhattan distance: ", final_Output[0][0]/5)
    print("BFS & Euclidean distance: ",final_Output[0][1]/5)
    print("BFS & Misplaced tiles: ",    final_Output[0][2]/5)


if __name__ == "__main__":
    main() 