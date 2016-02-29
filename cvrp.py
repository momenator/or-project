"""
A CVRP model with one depot 
Based on Implementation by Joao Pedro PEDROSO and Mikio KUBO
approach:
    - start with assignment model
    - add cuts until all components of the graph are connected
"""
import math
import random
import networkx
from gurobipy import *

"""
Parameters:
    - V: set/list of nodes in the graph
    - c[i,j]: cost for traversing edge (i,j)
    - m: number of vehicles available
    - q[i]: demand for customer i
    - Q: vehicle capacity
Returns the optimum objective value and the list of edges used.
"""
def solve_vrp(V,c,m,q,Q):
    
    """
        addcut: add constraint to eliminate infeasible solutions
        Parameters:
            - cut_edges: list of edges in the current solution, except connections to depot
        Returns True is a cut was added, False otherwise
    """   
    def addcut(cut_edges):
        G = networkx.Graph()
        G.add_edges_from(cut_edges)
        Components = networkx.connected_components(G)
        cut = False
        for S in Components:
            S_card = len(S)
            q_sum = sum(q[i] for i in S)
            NS = int(math.ceil(float(q_sum)/Q))
            S_edges = [(i,j) for i in S for j in S if i<j and (i,j) in cut_edges]
            if S_card >= 3 and (len(S_edges) >= S_card or NS > 1):
                # Subtour elimination constraint
                add = model.addConstr(quicksum(x[i,j] for i in S for j in S if j > i) <= S_card-NS)
                model.update()
                cut = True
        return cut

    model = Model("vrp")
    # x = 1 if there is an optimal path from i to j, 0 otherwise. 
    # Also it is restricted to Integer value
    x = {}
    for i in V:
        for j in V:
            if j > i and i == V[0]:       # depot
                # upper bound is 2 to account for incoming and outcoming vehicles
                x[i,j] = model.addVar(ub=2, vtype="I", name="x(%s,%s)"%(i,j))
            elif j > i:
                x[i,j] = model.addVar(ub=1, vtype="I", name="x(%s,%s)"%(i,j))
    
    model.update()

    # number of vehicle coming in == number of vehicle coming out.
    # So there are 2 * m paths in and out of the depot
    model.addConstr(quicksum(x[V[0],j] for j in V[1:]) == 2*m, "DegreeDepot")
    
    for i in V[1:]:
        model.addConstr(quicksum(x[j,i] for j in V if j < i) +
                        quicksum(x[i,j] for j in V if j > i) == 2, "Degree(%s)"%i)

    # Objective function
    model.setObjective(quicksum(c[i,j]*x[i,j] for i in V for j in V if j>i), GRB.MINIMIZE)

    model.update()
    # model.Params.OutputFlag = 0 # silent mode
    
    # Optimise until no more cuts can be added
    EPS = 1.e-6
    while True:
        model.optimize()
        edges = []
        for (i,j) in x:
            if x[i,j].X > EPS:
                if i != V[0] and j != V[0]:
                    edges.append((i,j))
        if addcut(edges) == False:
            break

    return model.ObjVal,edges

def make_data(infile, numNodes):
    # it's easier to label the nodes with number with node 0 as the depot
    V = range(1,numNodes)
    distanceDict = {}
    for line in infile:
        line.replace("\n","")
        lineArg = line.split(" ")
        distanceDict[(int(lineArg[0]), int(lineArg[1]))] = int(lineArg[2])

    print distanceDict
    c,q = {},{}
    Q = 15
    for i in V:
        # sets the demand for all depots to be 1
        q[i] = 1
        for j in V:
            # skips if j < i
            if j > i:
                c[i,j] = distanceDict[(i,j)]
    return V,c,q,Q
    
            
if __name__ == "__main__":
    from sys import argv

    script, datafile = argv
    
    inputData = open(datafile)
    m = 16
    V,c,q,Q = make_data(inputData, 227)
    z,edges = solve_vrp(V,c,m,q,Q)
    print ("Optimal solution:" , z)
    print ("Edges in the solution:")
    print (sorted(edges))
    print ("Edges:")
    print (edges)