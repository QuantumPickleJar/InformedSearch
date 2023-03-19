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

    #Reference: https://www.engineeringenotes.com/artificial-intelligence-2/state-space-search/notes-on-water-jug-problem-artificial-intelligence/34582#:~:text=The%20state%20space%20for%20this,in%20the%203%2Dgallon%20jug.
    a = 0; b = 0; # current amount of water in jugs
    jugA = 9; jugB = 4 # jug capacity

    def __init__(self, initial, goal):
        Problem.__init__(self,initial, goal)


    # Builds a list of actions from which to choose from 
    def actions(self, state):

        list=[] # store the list of actions here

        a = state[JugProblem.a]; b = state[JugProblem.b]

        # are we at the goal state?
        if a == self.goal: 
            print("goal reached", a, b)
            return

        # can we fill A?
        if self.validate_state(a + (self.jugA - a), b):
            list.append("a_max")

        # can we fill B?
        if self.validate_state(a, b + (self.jugB - b)):
                list.append("b_max")

        # can we completely empty A?
        if self.validate_state(0, b):
             list.append("a_dump_all")

        # can we completely empty B?
        if self.validate_state(a, 0):
             list.append("b_dump_all")
   
        # # can we completely empty A?
        # if self.validate_state(a - self.jugA, b):
        #      list.append("a_dump_all")

        # # can we completely empty B?
        # if self.validate_state(a, b - self.jugB):
        #      list.append("b_dump_all")

        # can we empty some of A into B?
        if self.validate_state(a - (self.jugB - b), b):
            list.append("part_a_to_b")

        # can we empty some of B into A?
        if self.validate_state(a, b - (self.jugA - a)):
            list.append("part_b_to_a")  

        # can we empty all of A into B?
        if self.validate_state(0, b + a):
            list.append("a_to_b")

        # can we empty all of B into A?
        if self.validate_state(a + b, 0):
            list.append("b_to_a")  
        return list



    # a - what is being done to the water in jug a
    # b - what is being done to the water in jug b
    def validate_state(self, a, b):
        # verify capacity of jugs doesn't exceed max
        if a > self.jugA or b > self.jugB: 
            return False 
        
        # verify no negative quanitities
        if a < 0 or b < 0: 
            return False
        
        # jug can't be empty when pouring into another


        return True

    def result(self, state, action):

        a, b = state[JugProblem.a], state[JugProblem.b]

        if action == "a_max":
            newState = (self.jugA, b)
        elif action == "b_max":
            newState = (a, self.jugB)
        elif action == "a_dump_all":
            newState = (0, b)
        elif action == "b_dump_all":
            newState = (a, 0)
        elif action == "part_a_to_b":
            newState = (a - a, a + b)
        elif action == "part_b_to_a":
            newState = (a + b, b - b)
        elif action == "a_to_b":
            newState = (0, b + a)
        elif action == "b_to_a":
            newState = (a + b, 0)
        return newState
        

def main():
    print('Testing the Jug problem')
    
    initState = (0,0)
    goalState = (6,0)

    #define the problem in terms of current and goal state
    problem = JugProblem(initState, goalState)
    
    #Once the problem is created, we cna perform a search on it
    #goal = iterative_deepening_search(problem)
    goal = breadth_first_search(problem)

    print("\nPath = ", goal.path(),"\n\nPath cost = ", goal.path_cost)
    print()
    print("\nSolution = ",goal.solution())

    print("Initial state: ", initState,"Goal state:", goalState)
main()