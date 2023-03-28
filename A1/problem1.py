from search import Problem, iterative_deepening_search, breadth_first_search
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

    a,b = 0,0 # current amount of water in jugs
    jugA = 9; jugB = 4 # jug capacity

    def __init__(self, initial, goal):
        Problem.__init__(self,initial, goal)


    """Return True if the state is a goal.""" 
    def goal_test(self, state):
        return state[0] == 6

    # Builds a list of actions from which to choose from 
    def actions(self, state):

        list=[] # store the list of actions here

        # are we at the goal state?
        if self.goal_test(state):
            print("goal reached", state[0], state[1])
            return list

        a = state[0]; b = state[1]


        # can we fill A?
        if a < self.jugA:
            list.append("a_max")

        # can we fill B?
        if b < self.jugB:
            list.append("b_max")

        # can we completely empty A?
        if a > 0:
             list.append("a_dump_all")
             

        # can we completely empty B?
        if b > 0:
             list.append("b_dump_all")
             
        
        ### Target block
        # can we empty all (or some) of A into B?
        if a > 0 and b < self.jugB:
            #if a + b <= self.jugB:
                list.append("a_to_b")
            # (a >= self.jugB - b or (a + b) >= self.jugB
            
        ### End target block

        # can we empty all (or some) of B into A?
        if b > 0 and a < self.jugA and  \
            (b >= self.jugA - a or b == self.jugB):
             list.append("b_to_a")

        # # this first predicate handles adding to B when B is zero
        # if (a != 0 and b == 0) or   \
        #     b < self.jugB and a != 0: #and (self.jugB - b) + a <= self.jugB):
        #         list.append("a_to_b")

        ''' 
            A must not be full
            A must have room for B
            B must be non-zero 
            adding B to A must not exceed A_max (handled in results)
        '''
        # can we empty all of B into A?
         
        # # this first predicate handles adding to A when A is zero
        # if (a == 0 and b != 0) or \
        #     a < self.jugA and b != 0: # and (self.jugA - a) + b <= self.jugA:
        #         list.append("b_to_a")  
        return list



    def result(self, state, action):
        newState = state

        a, b = state[0], state[1]

        if action == "a_max":
            newState = (self.jugA, b)
        elif action == "b_max":
            newState = (a, self.jugB)
        elif action == "a_dump_all":
            newState = (0, b)
        elif action == "b_dump_all":
            newState = (a, 0)
        ### Target block
        elif action == "a_to_b":
            b_vol_left = self.jugB - b
            
            b = min(a + b, self.jugB)
            a = max(a - b_vol_left, 0)
            newState = (a, b)
        ### End target block

        elif action == "b_to_a":
            a_vol_left = self.jugA - a
            
            a = min(a + b, self.jugA)
            b = max(b - a_vol_left, 0)
            newState = (a, b)

        return newState
        

def main():
    print('Testing the Jug problem')
    
    initState = (0,0)
    goalState = (6,0)

    #define the problem in terms of current and goal state
    problem = JugProblem(initState, goalState)
    
    #Once the problem is created, we cna perform a search on it
    goal = iterative_deepening_search(problem)
    print("\nPath = ", goal.path(),"\n\nPath cost = ", goal.path_cost)
    print()
    print("\nSolution = ",goal.solution())

    print("Initial state: ", initState,"Goal state:", goalState)
main()