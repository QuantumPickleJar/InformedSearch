from search import *
from timeit import default_timer as timer
#______________________________________________________________________________
# Code to compare searchers on various problems.
class InstrumentedProblem(Problem):
    """Delegates to a problem, and keeps statistics."""

    def __init__(self, problem):
        #succs - nodes expanded 
        #states - nodes generated
        #goal_tests - number of times goal is tested
        self.problem = problem
        self.succs = self.goal_tests = self.states = self.final_cost = 0
        self.found = None
        self.start = timer()
        self.duration = 0

    def actions(self, state):
        self.succs += 1
        return self.problem.actions(state)

    def result(self, state, action):
        self.states += 1
        return self.problem.result(state, action)

    def goal_test(self, state):
        self.goal_tests += 1
        result = self.problem.goal_test(state)
        if result:
            self.found = state
            self.duration = timer() - self.start
        return result

    def path_cost(self, c, state1, action, state2):
        return self.problem.path_cost(c, state1, action, state2)

 
    def __getattr__(self, attr):
        return getattr(self.problem, attr)
                         
    def __repr__(self):
        return '<%4d/%4d/%4d/%4d/%4d>' % (self.succs, self.goal_tests,self.states, self.final_cost, int(self.duration))
    
    def getStats(self):
        return (self.succs, self.goal_tests,self.states, self.final_cost)
    
def name(obj):
    try:
        return obj.__name__
    except:
        return str(obj)

def print_table(table, header=None, key=None):
    """Print a list of lists as a table, so that columns line up nicely.
    header, if specified, will be printed as the first row."""
    if key:
        print ("%60s" % key)
    if header:
        table = [header] + table
    i=0
    for row in table:
        j=0
        for s in row:
            print ("%26s" % s, end="")
            j+=1
        i+=1
        print()
    print()

#Batch processor to run multiple problems and algorithms
def compare_searchers(problems, header,
                      searchers=[breadth_first_search, depth_first_search]):
    def do(searcher, problem):
        p = InstrumentedProblem(problem)
        g=searcher(p)
        p.final_cost=g.path_cost
        return p
    table = [[name(s)] + [do(s, p) for p in problems] for s in searchers]
    print_table(table, header,"Expanded/Goal Tests/Generated/Cost/Duration")
#______________________________________________________________________________
