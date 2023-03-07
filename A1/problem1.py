from search import Problem

# model problem 1 as a class
'''
You have two jugs measuring 4 and 9 liters. Both jugs are initially empty; assume you have
an unlimited supply of water, and can empty jugs as often as desired. You want to measure
out exactly 6 liters.

Model this as a search problem, using the provided code base; then run an uninformed search
algorithm on the problem to print the optimal solution. You should display the steps to reach
the goal and the total number of steps taken. Code this in a file called problem1.py that you
provide.'''

'''TODO: 
    You should subclass this and implement the methods actions and result, 
    and possibly __init__, goal_test, and path_cost. Then you will create 
    instances of your subclass and solve them with the various search functions
'''
class JugProblem(Problem):

    #Reference: https://www.engineeringenotes.com/artificial-intelligence-2/state-space-search/notes-on-water-jug-problem-artificial-intelligence/34582#:~:text=The%20state%20space%20for%20this,in%20the%203%2Dgallon%20jug.

    def __init__(self, initial, goal):
        Problem.__init(self,initial,goal)
        jugA = 0 # holds 4L
        jugB = 0 # holds 9L
        
        initState = (0,0) # define our start state (both jugs are empty)
        goalState = (0,6) # define our goal state (jug B holds 6L)



    def actions(self, state):

        # if jugA is full:

        # if jugB is full:


    def result(self, state, action):

        '''
        State space planning:
        let's determineour choices given the two jugs:
        Start: (0, 0)
                
        
        '''
        return newState


    def main():
        print('Testing the Jug problem')
        #print("Initial state: ", initState,"Goal state:", goalState)
        