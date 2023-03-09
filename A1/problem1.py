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
    a = 0; b = 0; # starting amount of water in jugs
    jugA = 9; jugB = 4 # jug capacity


    def __init__(self, initial, goal):
        Problem.__init__(self,initial,goal)



    # Builds a list of actions from which to choose from 
    def actions(self, state):

        list=[] # store the list of actions here

        a = state[JugProblem.a]; b = state[JugProblem.b]

        # 1 - fill jug A fully
        if self.validate_state(a + 4, b):
            # the string returned will be identified in results NOT USED ANYWHERE ELSE  
            list.append() # remember, the string use here is to help identify programmatic flow


        # if jugA is full:

        # if jugB is full:
        return list

    # a - what is being done to the water in jug a
    # b - what is being done to the water in jug b
    def validate_state(self, a, b):
        
        if a > 9 or b > 6: # Capcity constraint
            return False 
        #

    def result(self, state, action):

        '''
        State space planning:
        let's determine our choices given the two jugs:
        Start: (0, 0)
                
        
        '''
        return newState


    def main():
        print('Testing the Jug problem')
        #print("Initial state: ", initState,"Goal state:", goalState)
        '''
        Desired output:
        (a,b)'''