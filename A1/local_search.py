import sys, math, random
from utils import *
from search import *

#Possible schedule functions   
def exp_schedule1(t=0, k=20, limit=100):
    """Basic schedule function for simulated annealing"""
    return lambda t: (k/(1+t) if t < limit else 0)

def exp_schedule2(t=0,k=20, lam=0.005, limit=100):
    """Another possible schedule function for simulated annealing"""
    return lambda t: (k * math.exp(-lam * t) if t < limit else 0)

#Simulated annealing algorithm
def simulated_annealing(problem, schedule=exp_schedule2()):
    '''returns a tuple with final state, final state value and time t'''
    current = Node(problem.initial)
    state = current.state

    for t in range(sys.maxsize):
        T = schedule(t)
        if T == 0:
            return (current.state, problem.value(current.state),t)
            
        #For true SA, this line is not there as we usually don't know the optimal value for the goal state
        #So, if you don't know the optimal, the goal_state should always return false
        if problem.goal_state(state):
            return (current.state, problem.value(current.state),t)
            
        neighbors = current.expand(problem)
        
        if not neighbors:
            return (current.state, problem.value(current.state),t)
            
        next_choice = random.choice(neighbors)
        delta_e = problem.value(next_choice.state) - problem.value(current.state)
        if delta_e > 0 or probability(math.exp(delta_e / T)):
            current = next_choice

###########################################################
#Problem 3
#Complete the NQueen problem below
class NQueenProblem(Problem):
    '''
    The problem of placing N queens on an NxN board with none attacking
    each other.  The problem can be initialized to some random, non-viable state.
    A state is represented as an N-element array, where a value of r in the c-th 
    entry means there is a queen at column c, row r. 
    '''
    def __init__(self, N, init):
        self.N = N
        self.initial = init



    '''
        Note:
        The actions method may be used in some other recursive function in order 
        to achive backtracking, but it will be used outside of the backtracking 
        to generate the initial set of moves from the initial state.
    '''
    def actions(self, state):
        '''
        Implement this method.
        Returns the neighbors of a given state. You must implement this so that the
        neighbors are from the "neighborhood" and are not an enormous set.
        '''
        valid_moves = []

        # Start by placing the first queen and building our search tree

        # noQueens is one-based, so checking [i-1] columns would actually be [0-(i-2)]

        # THIS is how we iterate over the 1D board.  i,j indices are for 2D...
        for row, col in enumerate(state):

            # Check all the rows for this column
            for next_row in self.N:

                # check if placing queen at next_row is safe
                if not self.conflict(next_row, col, row, col):
                    # The move must be valid, add it to moves!
                    valid_moves.append((next_row, col))

            next_row = row
            # Check all the columns for this row
            for next_col in self.N:
                # check if placing queen at next_col is safe
                if next_col != col and not self.conflict(row, next_col, row, col):
                    # The move must be valid, add it to moves!
                    valid_moves.append((next_row, next_col))

        # return the neighbors of a given state
        return valid_moves
        

    # Separate from result(), we need to probe the state space 
    
    # returns a solution or a failure
    def backtrack_search_init(self, state):
        init_state = [None] * self.N
        return self.backtrack_search(init_state)

    '''
    Recursively searchs for possible solutions viabacktracking. 
    '''
    def backtrack_search(self, state):
        # [ BASE CASE ]
        # if all queens placed, return the state
        if self.isSolution(state):
            # Make sure that the solution is valid first
            if(self.goal_test(state)):  #TODO:  MAY NEED TO REMOVE THIS LINE
                return state            
            else: 
                return None        
            
        pending_queen_index = self.get_pending_queen_index(state)

        # [ RECURSIVE CASE ]
        # if there are still queens that have not been placed,
        # try to place them in a safe column.
        for col in range(self.N):
            if not self.is_unsafe(state, pending_queen_index, col):

                new_state = state.copy()
                new_state[pending_queen_index] = col
                
                result = self.backtrack_search(new_state)
                if result is not None:
                    return result

        # if there are no more queens to place, return None
        return None
 
    # Returns the index of the queen that must be placed next
    def get_pending_queen_index(self, state):
        for i in range(len(state)):
            if state[i] == None:
                return i
        return None


    # Determines if the state has all four queens placed
    def isSolution(self, state):
        if None in state:
            return False
        else:
            return True


    def result(self, state, action):
        ''' Modify this if your result state is different from your action'''
        # incoming looks like '(x, y)'

        # state[x] should become y, ergo:
        new_state = state.copy()
        new_state[action[0]] = action[1]
        return new_state

    def goal_state(self, state):
        return self.goal_test(state)
    
    def goal_test(self, state):
        """Return True if the state is a goal. The number of non-conflicts is N*(N-1)/2""" 
        if self.value(state) == self.N*(self.N-1)/2:
            return True
        return False
 
    # Takes a state as input
    def value(self, state):
        '''
        Implement this method.
        Assigns a value to a given state that represents the number of non-conflicts.
        The higher the better with the maximum being (N*(N-1))/2 
        '''
        # We can assume a perfect board, then tally conflicts 
        count = (self.N * (self.N - 1)) / 2

        # loop through all of the rows columns and count the number of non-conflicting queens
        for row, col in enumerate(state):
            # Does the current queen conflict with where 
            # the new queen will be placed?
            if self.conflict(row, col, state[row], state[col]):
                count -= 1
        return count


    '''returns true if a queen at [row1,col1] would conflict with the cell at [row2,col2]?'''
    def conflict(self, row1, col1, row2, col2):    
        
        return (row1 == row2 ## same row
                or col1 == col2 ## same column
                or row1-col1 == row2-col2  ## same \ diagonal
                or row1+col1 == row2+col2) ## same / diagonal
    
    #You may add other helper methods in this class

    # Check if placing a queen at row, col is unsafe with any queens
    def is_unsafe(self, state, row, col):
        for i in range(self.N):
            if state[i] is not None and self.conflict(i, state[i], row, col):
                return True
            return False

    def get_valid_init_state(self, state):
        
        while True:
            state = generateNQueenState(self.N)
            if not any(self.conflict(state[i], i, state[j], j)
                for i in range(self.N) \
                    # start from i + 1 to avoid checking pairs twice
                    for j in range(i + 1, self.N) if i < j):
                return state
            
            '''
                Wow!  Python is incredible... using 'List Comprehension'
                we can generate a new state with appropriately ranged values 
                that are zero-based) 
            '''
            state = [random.randrange(self.N) for i in range(self.N)]



############################################################ 

#utility method to generate random NQueen states; ignore if you wish
def generateNQueenState(N):
    '''Generates a random NQueen state; might be non-viable'''
    state = []
    for i in range(N):
        state.append(random.randrange(N))
    return state
############################################################ 
#Problem 3
#Use completed NQueen problem and SA to solve the problem for N=4 and N=8
#Provide sample starting states for both instances
def main():
    

    #init_state = generateNQueenState(4)
    problem = NQueenProblem(4,None)
    init_state = problem.get_valid_init_state(4)
    #init_state = [2,0,3,1] # DEBUG LINE
    print(init_state)
    problem = NQueenProblem(4, init_state)

    four_result = simulated_annealing(problem, exp_schedule1())
    four_result2 = simulated_annealing(problem, exp_schedule2())

    # eight_result = simulated_annealing(problem, exp_schedule2())
    print(f"4-Queen solution for the first annealing schedule: {four_result}")

    '''
        state = RHState(grid)
        print(state)
    '''
    
main()