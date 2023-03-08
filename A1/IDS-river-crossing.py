from search import Problem, breadth_first_search,depth_first_search, iterative_deepening_search

#______________________________________________________________________________
#An implementation of the Banker-Robber problem
# Tuple format = [<Node (leftBankers, rightBankers, leftRobbers, rightRobbers, boatSide)>]
class BRP(Problem):
    # STATE REPRESENTATION OF THE PROBLEM #
    #state is a tuple(LB,RB,LR,RR,B) with initial value (0,3,0,3,1)
    #last value flips between 1(R) and 0(L)   
    LB=0; RB=1; LR=2; RR=3; B=4 #class "constants"
    
    def __init__(self, initState,goalState):
    	Problem.__init__(self, initState, goalState)
    
    # Decisional logic
    def actions(self, state):     
        # In this kind of simple example, it is common to use the new state itself as the action, 
        # because it is straightforward and more efficient.
        # We don't do that here just to illustrate how we can denote actions separately from states, if so desired.
        
        # list of descriptive actions
        list=[]
        #temp variables for clarity:
        lb, rb, lr, rr, boat = state[BRP .LB], state[BRP.RB], state[BRP.LR],state[BRP.RR], state[BRP.B]
        
        if boat == 1: #boat on the right side
            #1BL - can we move 1 Banker left?
            if self.validate(lb+1, rb-1, lr, rr, 0):
                list.append("1BL")
                
            #2BL - can we move 2 Bankers left?
            if self.validate(lb+2, rb-2, lr, rr, 0):
                list.append("2BL")   
                
            #1RL - can we move one Robber left?
            if self.validate(lb ,rb, lr+1, rr-1, 0):
                list.append("1RL")
                
            #2RL - can we move two Robbers left?
            if self.validate(lb, rb, lr+2, rr-2, 0):
                list.append("2RL")     
                
            #1B1RL -  can we move one Banker and one Robber left?
            if self.validate(lb+1, rb-1, lr+1, rr-1, 0):
                list.append("1B1RL")   
                
        else:   #boat on the left side
            #1BR - can we move 1 Banker right?
            if self.validate(lb-1, rb+1, lr, rr, 1):
                list.append("1BR")
                
            #2BR - can we move 2 Bankers right?
            if self.validate(lb-2, rb+2, lr, rr, 1):
                list.append("2BR")    
                
            #1RR - can we move 1 Robber right?
            if self.validate(lb, rb, lr-1, rr+1, 1):
                list.append("1RR")
                
            #2RR - can we move 2 Robbers right?
            if self.validate(lb, rb, lr-2, rr+2, 1):
                list.append("2RR")    
                
            #1B1RR-  can we move one Banker and one Robber right?
            if self.validate(lb-1, rb+1, lr-1, rr+1, 1):
                list.append("1B1RR")   
                
        return list

    def validate(self, lb, rb, lr, rr, boat):
        #verify no number is negative
        if lb < 0 or rb < 0 or lr < 0 or rr < 0:
            return False
        #verify no number is greater than the max
        if lb > 3 or rb > 3 or lr > 3 or rr > 3:
            return False
        #verify if boat is on right, then there must be someone on the right side
        if boat == 1 and (rb + rr)==0:
            return False
        #verify if boat is on left, then there must be someone on the left side
        if boat == 0 and (lb + lr)==0:
            return False
        #verify left Bankers are >= left Robbers, unless there are no Bankers on the left
        if lb < lr and lb != 0:
            return False
        #verify right Bankers are >= right Robbers, unless there are no Bankers on the right
        if rb < rr and rb != 0:
            return False
        return True  
        
        
    def result(self, state, action):
        #Inefficient because we are redoing what we did in actions, but this keeps actions distinct from states
        #Again, temp variables for clarity:
        lb, rb, lr, rr, boat = state[BRP.LB], state[BRP.RB], state[BRP.LR],state[BRP.RR], state[BRP.B]
        
        if action=="1BL":
            newState = (lb+1, rb-1, lr, rr, 0)
        elif action=="2BL": 
            newState = (lb+2, rb-2, lr, rr, 0)
        elif action=="1RL": 
            newState = (lb ,rb, lr+1, rr-1, 0)
        elif action=="2RL": 
            newState = (lb, rb, lr+2, rr-2, 0)        
        elif action=="1B1RL": 
            newState = (lb+1, rb-1, lr+1, rr-1, 0)       
        elif action=="1BR":
            newState = (lb-1, rb+1, lr, rr, 1)    
        elif action=="2BR":  
            newState = (lb-2, rb+2, lr, rr, 1)
        elif action=="1RR": 
            newState = (lb, rb, lr-1, rr+1, 1)
        elif action=="2RR":
            newState = (lb, rb, lr-2, rr+2, 1)
        elif action=="1B1RR":
            newState = (lb-1, rb+1, lr-1, rr+1, 1)

        return newState 

def main():
    #Runs the Robbers and Bankers problem, will provide a solution to getting all Bankers
    #and all Robbers to the other side, without Bankers ever being outnumbered by Robbers
    #on either side.
    print('Bankers/Robbers Problem: ')
    print(' Tuples are in this format --> [<Node (leftBankers, rightBankers, leftRobbers, rightRobbers, boatSide)>]')
    initState = (0,3,0,3,1)
    goalState = (3,0,3,0,0)

    #define the problem in terms of current and goal state
    problem = BRP(initState, goalState)
    
    #Once the problem is created, we cna perform a search on it
    goal = iterative_deepening_search(problem)
    print("\nPath = ",goal.path(),"\n\nPath cost = ",goal.path_cost)
    print()
    print("\nSolution = ",goal.solution())

main()