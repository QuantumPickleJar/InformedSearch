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
        actions = []
        
        # if you change one action, you must change all of them
        # determine where cars can go 
        for car in state.cars:
            x = car.left
            y = car.top
        
            # horizontal 
            if car.orientation: 
                # check left
                if x > 0:
                    # check if space is empty
                    if state.grid[y][x - 1] == -1:
                        # actions.append((car, 0, -1))
                        actions.append((car.id, 'left'))

                # check right         
                if x + car.L < len(state.grid):
                    # check if space is empty
                    if state.grid[y][x + car.L] == -1:
                        # actions.append((car, 0, 1))
                        actions.append((car.id, 'right'))
            else:     
                # check above the car  
                if y > 0:
                    # check if space is empty
                    if state.grid[y - car.L][x] == -1:
                        # actions.append((car, 1, 0))
                        actions.append((car.id, 'up'))                        

                # check below the car  
                if y + car.L < len(state.grid):
                    # check if space is empty
                    if state.grid[y - car.L][x] == -1:
                        # actions.append((car, 1, 0))
                        actions.append((car.id, 'down'))                        

    def goal_test(self, state):  
        #is the red car EXACTLY where it needs to be on the grid, in the right orientation?
        if state.cars[0].left == 2 and state.cars[0].top == 5:
            return True
        else:
            return False

    # must advance to the next state based on the action taken from the current state
    def result(self, state, action):
        # parse the top and left modification from the action

        # apply the move to the car based on the action
        car_id, dx, dy = action
        result_grid = [row[:] for row in state.grid]

        car = state.cars[car_id]
        top, left, L, orientation = car.top + dy, car.left + dx, car.L, car.orientation

        # first, update empty spaces to reflect the move
        if orientation:
            for j in range(left, left + L):
                result_grid[top][j] = -1
        else:
            for i in range(top, top + L):
                result_grid[i][left] = -1

        # for i in range(top, top + L):
        #     for j in range (left, left + L):
        #         result_grid[i][j] = -1

        # send new coordainates 
        if orientation:
            for j in range(left + dx, left + L + dx):
                result_grid[top + dy][j] = id
        else:
            for i in range(top + dy, top + L + dy):
                # result_grid[i][left + dx] = id
                result_grid[i][left] = id




        # for i in range(top, top + L):
        #     for j in range(left, left + L):
        #         result_grid[i][j] = car_id
        '''
        car = state.cars[car_id]

        # if the action calls for this car to move:
        if car.orientation: 
        if move == 'left':
            result_grid[car.top][car.left - 1] = car.id
            # update empty cell
            
            result_grid[car.top][car.left + car.L - 1] = -1     
            # update the car's property to reflect the move
            car.left -= 1

        else: # move = right 
            result_grid[car.top][car.left + car.L] = car.id
            result_grid[car.top][car.left] = -1     
            # update the car's property to reflect the move
            car.left += 1
        else: 
        if move == 'up':
            result_grid[car.top - 1][car.left] = car.id
            result_grid[car.top + car.L - 1][car.left] = -1     
            car.left -= 1

        else:  # move = down
            result_grid[car.top + car.L][car.left] = car.id
            result_grid[car.top][car.left] = -1     
            # update the car's property to reflect the move
            car.top += 1
        '''
 

        # initalize the problem with the new grid
        
        new_state = RHState(result_grid)
        
        return new_state
                    

    '''
        Heuristic that is admissible because it never overestimates distance to goal;
        other cars can only block and do not reduce the distance to the goal.
    '''
    
    def h(self, node):
        car_red = node.state.cars[0]
        dist = len(node.state.grid) - car_red.left - car_red.L
        return dist
    
        # alternate heuristic ideas:
        # what if we weighted vehicles by their L and use this to calcualte a weighted path to goal position?
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

    problem = RushHour(state,0)
    
    start = timer()
    goal = astar_search(problem)
    print("\nPath = ",goal.path(),"\n\nPath cost = ",goal.path_cost)
    print()
    print("\nSolution = ",goal.solution())
 
    end = timer()
    print("Time taken:",end - start)
    
    
main()