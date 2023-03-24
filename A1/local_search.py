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


    def actions(self, state):
        '''
        Implement this method.
        Returns the neighbors of a given state. You must implement this so that the
        neighbors are from the "neighborhood" and are not an enormous set.
        '''
        valid_moves = []


        # Start by placing the first queen and building our search tree
        for i in range(self.N):
            for j in range(self.N):
                if not self.conflict(i,j, state[i], state[j]):
                    valid_moves.append((i,j))


        # return the neighbors of a given state
        return valid_moves
        
            
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


        '''
        Right now, we are performing a Cartesian check, when we instead want to check the '''



        for i in range(self.N):
            for j in range(self.N):
                # Does the current queen conflict with where 
                # the new queen will be placed?
                if self.conflict(i,j,state[i],state[j]):
                    count -= 1
        return count

    def conflict(self, row1, col1, row2, col2):    
        '''
        Utility method. You can use this in other methods.
        Would putting two queens in (row1, col1) and (row2, col2) conflict?
        '''
        return (row1 == row2 ## same row
                or col1 == col2 ## same column
                or row1-col1 == row2-col2  ## same \ diagonal
                or row1+col1 == row2+col2) ## same / diagonal
    
    #You may add other helper methods in this class


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
    init_state = [2,0,3,1]
    print(init_state)
    problem = NQueenProblem(4, init_state)
    simulated_annealing(problem, exp_schedule1())

    '''
        state = RHState(grid)
        print(state)
    '''
    
main()