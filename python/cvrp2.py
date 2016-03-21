import math
import random
import networkx
from gurobipy import *

class CVRPGurobi:
	"""
		A CVRP model with one depot
		Based on Implementation by Joao Pedro PEDROSO and Mikio KUBO
		approach:
			- start with assignment model
			- add cuts until all components of the graph are connected
	"""
	def __init__(self,nodes,m,Q):
		"""
			Parameters:
				- nodes: set/list of nodes in the graph
				- m: number of vehicles available
				- Q: vehicle capacity
		"""
		self._nodes = nodes
		self._V = []
		self._c = {}
		self._m = m
		self._q = {}
		self._Q = Q
		# Gurobi VRP model
		self._model = Model("vrp")
		# Dictionary to mark the optimal paths
		self._x = {}

		# Time window variables and constraints
		# Dictionary for time window constraints
		self._u = {}
		self._e = {}
		self._l = {}

		self._objective_value = 0
		self._E = {}

	def add_cut(self, cut_edges):
		"""
			add_cut: add constraint to eliminate infeasible solutions
			Parameters:
				- cut_edges: list of edges in the current solution, except connections to depot
			Returns True is a cut was added, False otherwise
		"""
		G = networkx.Graph()
		G.add_edges_from(cut_edges)
		Components = networkx.connected_components(G)
		cut = False
		for S in Components:
			S_card = len(S)
			q_sum = sum(self._q[i] for i in S)
			NS = int(math.ceil(float(q_sum)/self._Q))
			S_edges = [(i,j) for i in S for j in S if i<j and (i,j) in cut_edges]
			if S_card >= 3 and (len(S_edges) >= S_card or NS > 1):
				# Subtour elimination constraint
				add = self._model.addConstr(quicksum(self._x[i,j] for i in S for j in S if j > i) <= S_card-NS)
				self._model.update()
				cut = True
		return cut

	def add_path_variables(self):
		"""
			add_path_variables: add model variables given the path constraints and updates
			the Gurobi model once at the end
		"""
		for i in self._V:
			for j in self._V:
				if j != i and i == self._V[0]:       # depot
					# upper bound is 2 to account for incoming and outcoming vehicles
					self._x[i,j] = self._model.addVar(ub=2, vtype="I", name="x(%s,%s)"%(i,j))
				elif j != i:
					self._x[i,j] = self._model.addVar(ub=1, vtype="I", name="x(%s,%s)"%(i,j))

		self._model.update()

	def add_vehicle_constraints(self):
		"""
			add_vehicle_constraints: add vehicle constraints to the model and updates the Gurobi
			model once at the end
		"""
		# number of vehicle coming in == number of vehicle coming out.
		# So there are 2 * m paths in and out of the depot
		self._model.addConstr(quicksum(self._x[self._V[0],j] for j in self._V[1:]) == 2*self._m, "DegreeDepot")

		for i in self._V[1:]:
			self._model.addConstr(quicksum(self._x[j,i] for j in self._V if j < i) +
				quicksum(self._x[i,j] for j in self._V if j > i) == 2, "Degree(%s)"%i)
		self._model.update()

	def add_tw_constraints(self):
		for i in self._V:
			for j in self._V:
				if i != j:
					self._u[i,j] = self._model.addVar(vtype="C", name="u(%s,%s)"%(i,j))

		self._model.update()

		for j in range(2, self._nodes+1):
			self._model.addConstr(quicksum(self._u[i,j] + self._c[i,j]*self._x[i,j] for i in range(1,self._nodes+1)
										   if i != j) - quicksum(self._u[j,k] for k in range(1,self._nodes+1)
																 if k != j) <= 0, "Relate(%s)"%j)

		print self._l

		for i in range(1,self._nodes+1):
			for j in range(1,self._nodes+1):
				if i != j:
					self._model.addConstr(self._e[i]*self._x[i,j] <= self._u[i,j], "LB(%s,%s)"%(i,j))
					self._model.addConstr(self._u[i,j] <= self._l[i]*self._x[i,j], "UB(%s,%s)"%(i,j))
		self._model.update()

	def add_objective_function(self):
		"""
			add_objective_function: add objective function and updates the Gurobi model once at the end
		"""
		# Objective function
		self._model.setObjective(quicksum(self._c[i,j]*self._x[i,j] for i in self._V for j in self._V if j>i), GRB.MINIMIZE)
		self._model.update()

	def optimise(self):
		"""
			optimise: Optimise the model by adding cuts continuously into the model until no more them can be added
		"""
		EPS = 1.e-6
		while True:
			self._model.optimize()
			edges = []
			for (i,j) in self._x:
				if self._x[i,j].X > EPS:
					if i != self._V[0] and j != self._V[0]:
						edges.append((i,j))
						self._E[(i,j)] = 1
			if self.add_cut(edges) == False:
				break
		# model.ObjVal,edges
		self._objective_value = self._model.ObjVal

	def make_cost_matrix(self,inDict):
		"""
			make_cost_matrix: fill in the cost matrix to the instance of CVRPGurobi class
			Parameters:
				- distanceDict: a dictionary with the tuple (i, j) as the key that specifies
				the path in the graph and a positive integer value that specifies the path's cost.
		"""
		# it's easier to label the nodes with number with node 0 as the depot
		self._V = range(1, self._nodes + 1)
		for i in self._V:
			# sets the demand for all depots to be 1
			self._q[i] = 1
			for j in self._V:
				# skips if j < i
				if j != i:
					self._c[i,j] = inDict[(i,j)]
					#self._c[i,j] = distance(inDict[i]['x'], inDict[i]['y'], inDict[j]['x'], inDict[j]['y'])

	def set_tw_vars(self, e, l):
		self._e = e
		self._l = l

	def get_objective(self):
		"""
			get_objective: return objective value
			Returns the objective value of the model
		"""
		return self._objective_value

def distance(x1,y1,x2,y2):
	return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def parse_coordinates_matrix(infile):
	coordinatesDict = {}

	for line in infile:
		line.replace("\n","")
		lineArg = line.split(" ")
		coordinatesDict[int(lineArg[0])] = {'x':float(lineArg[1]) ,'y':float(lineArg[2])}
	return coordinatesDict

"""
	Auxiliary functions to help run the model
"""
def parse_travel_matrix(infile):
	"""
		parse_travel_matrix: parse input file into a dictionary
		Parameters: input file, which contains the travel matrix. No header is included!
		Returns the dictionary of travel matrix for make_cost_matrix method.
	"""
	distanceDict = {}

	for line in infile:
		line.replace("\n","")
		lineArg = line.split(" ")
		distanceDict[(int(lineArg[0]), int(lineArg[1]))] = int(lineArg[2])
	return distanceDict

def main(argv):
	script, datafile = argv
	inputData = open(datafile)
	myModel = CVRPGurobi(9, 3, 4)

	e = {1:0, 2: 0, 3: 0, 4:0, 5:0,6:0,7:0,8:0,9:0 }

	l = {1:20, 2: 20, 3: 20, 4:20, 5:20,6:20,7:20,8:20,9:20 }

	dDict = parse_travel_matrix(inputData)
	myModel.make_cost_matrix(dDict)
	myModel.set_tw_vars(e, l)
	myModel.add_path_variables()
	myModel.add_tw_constraints()
	myModel.add_vehicle_constraints()
	myModel.add_objective_function()
	myModel.optimise()
	print "Optimal solution:" , myModel.get_objective()
	print "Edges:", len(myModel._E)
	print "Xs", myModel._x
	paths = []
	for key in myModel._x:
		if myModel._x[key].getAttr('X') > 0:
			paths.append(key)
	print paths

if __name__ == "__main__":
	from sys import argv
	if (len(argv) > 1):
		main(argv)
	else:
		print "Usage: python script_file data_file"
