from search import *
from compare import InstrumentedProblem, compare_searchers
from timeit import default_timer as timer
import sys

#Utility class to store car details
class Car:
    def __init__(self, id, top, left, L, orientation):
        """
        Parameters
        id: int
            id# of car in input 
        top: int
            Row of the start of car 
        left: int
            Column of the start of car 
        L: int
            Length of the car
        orientation: boolean
            True if the car is horizontal
            False if the car is vertical
        """
        self.id = id
        self.top = top
        self.left = left
        self.L = L
        self.orientation = orientation
    
    def __str__(self):
        return str(self.id)+": ["+str(self.top)+","+str(self.left)+"], L="+str(self.L)+", "+str(self.orientation)

class RHState:
    "State representation for the RushHour game"
    def __init__(self, grid):
        self.grid = grid
        self.cars = self.createCars(self.grid)
        self.saved=''

    def __str__(self):
        if not self.saved: #optimized because creation of str is a time hog, and grids are essentially immutable in usage
            s = "\n"
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    s += "%3s"% self.grid[i][j]
                s += "\n"
            self.saved = s
        return self.saved

    def __eq__(self, other):
        return isinstance(other, RHState) and str(self) == str(other)
    
    def __hash__(self):
        return hash(str(self))     
        
    #Painful and inefficient function to convert grid into objects: car-id, top, left, length, orientation
    #Cars are placed in the list according to their car-ids so retrieval is straightforward
    #0 is red car that must be moved to the goal cell, [2,5] is goal cell, dimensions are NxN where N=6
    def createCars(self, table):
        cars = []
        for id in range(sys.maxsize):
            found = False
            #Pass through grid to find if car with id exists
            i=0
            while i < len(table) and not found:
                j = 0
                while j < len(table[i]) and not found:
                    if table[i][j] == id: #found a car with id 					
                        found = True
                        #find left/right bounds or top/bottom bounds
                        if (j-1>=0 and table[i][j-1]==id) or (j+1<len(table[i]) and table[i][j+1]==id):
                            orientation = True # horizontal
                            top = i
                                
                            k = j
                            while k>0 and table[i][k]==id:	
                                k=k-1
                            if table[i][k]==id:
                                left = k
                            else:
                                left = k+1
                            
                            k = j                        
                            while k<len(table[i])-1 and table[i][k]==id:	
                                k=k+1
                            if table[i][k]!=id:
                                k = k-1
                            
                            L = k-left+1
                                                    
                        else: #if table[i-1][j] == id || table[i+1][j] == id:
                            orientation = False # vertical
                            left = j
                                
                            k = i
                            while k>0 and table[k][j]==id:	
                                k=k-1
                            if table[k][j]==id:
                                top = k
                            else:
                                top = k+1
                            
                            k = i  
                            while k<len(table)-1 and table[k][j]==id:	
                                k=k+1
                            if table[k][j]!=id:
                                k = k-1
                                
                            L = k-top+1
                                
                        car = Car(id,top,left,L,orientation)                            
                        cars.insert(id, car) #insert car at exactly position id in the cars list
                            
                    j = j+1
                i = i+1
                
            #check if we have found all cars in the grid
            if not found:
                break
        return cars					

#Problem 2:  
#Complete this class       
class RushHour(Problem):
    "Representation of the RushHour problem"
    def __init__(self, initState, heuristic=0):
        Problem.__init__(self, initState)
        self.heuristic=heuristic
         
    def actions(self, state):     

        '''
         To make for simpler programming, recall that a 2D board is a matrix
         which can be flattened to a list of size i * j (where i and j are 
         dimensions of the board)  
         Thus, in a game board of size N*N, to access an element at row i and column j:  
                (i * N) +  j
        '''
        
        actions = []         # Tuple: { CarToMove, leftChange, topchange }
        
        # determine where the red car can go
        car_red = state.cars[0]

        # If the car is horizontal
        if car_red.orientation:         
            if car_red.left > 0:        # left is valid
                actions.append((car_red, -1, 0))

            # if car_red.left < (state.grid[car_red.left] * 6) - car_red.L:        # right is valid
            if car_red.left < state.grid - car_red.L:        # right is valid
                actions.append((car_red, 1, 0))
            
        else: # if the car is vertical 
            if car_red.top > 0:         # up is valid
                actions.append((car_red, 0, 1))
            
            # if car_red.top > (state.grid[car_red.top] * 6) - car_red.L:         # down is valid
            if car_red.top < state.grid - car_red.L:         # down is valid
                actions.append((car_red, 0, -1))
            
        
        # determine where OTHER cars can go 
        #pos[0] = left, pos[1] = top
        for car in state.cars:
            x = car.left
            y = car.top
            
            # horizontal 
            if car.orientation: 
                # check left
                if x > 0 and (state[x] * 6) + y - car.L == -1:
                    actions.append((car, -1, 0))

                if x < 0 and (state[x] * 6) - y - car.L == -1:
                    actions.append((car, 1, 0))
            else: #vertical        
                # (i * N) + j
                # check above the car  [(i * 6) + (j - 1)]
                if y > 0 and (state[x] * 6) + x - car.L:

                # check below the car  [(i * 6) + (j + 1)]
                if y > 0 and (state[x] * 6) + x + car.L:
                
        '''Complete'''

    def goal_test(self, state):  
        #is the red car EXACTLY where it needs to be on the grid, in the right orientation?
        '''Complete - Return True if the state is a goal. False otherwise'''
        
        
    # must advance to the next state based on the action taken from the current state
    def result(self, state, action):
        '''Complete'''

    #Override this to be something meaningful in your domain, if you extend this class"
    def h(self, node):
        '''Modify this to add other heuristics. You can use self.heuristic to switch between different heuristics'''    
        if (self.heuristic==0):
            return 0
 
######################################################

#utility method - read input file and convert it into a state/grid
def readGridFromFile(fileName):
    infile = open(fileName,"r")
    grid = []   
    for line in infile:
        dataLine = (line[:-1])
        if dataLine[0]=='#': #Comment line starts from column 0 with # in that column; skip these lines
            continue
        data = dataLine.split()
        columns = []
        for i in data:
            columns.append(int(i))
        grid.append(columns)
    infile.close()
    return grid

#Problem 3: modify this to demonstrate your code    
def main():
    '''
    #Example: Running multiple files   
    fileNames = ["puzzles/1.txt","puzzles/2.txt","puzzles/3.txt","puzzles/4.txt"]
    headings = ['Algorithm']+fileNames
    RHProblems = []
    for f in fileNames:
        grid = readGridFromFile(f)
        state = RHState(grid)
        RHProblems.append(RushHour(state,0)) #heuristic h0; change this to be your best heuristic
    compare_searchers(problems=RHProblems, header=headings, searchers=[astar_search])  
    '''
      
    #Example: Running a single file
    grid = readGridFromFile("A1/puzzles/3.txt")
    state = RHState(grid)
    print(state)
    
    for i in state.cars:
        print(i)

    problem = RushHour(state)
    
    start = timer()
    goal = astar_search(problem)
    print("\nPath = ",goal.path(),"\n\nPath cost = ",goal.path_cost)
    print()
    print("\nSolution = ",goal.solution())
 
    end = timer()
    print("Time taken:",end - start)
    
    
main()