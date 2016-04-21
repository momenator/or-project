import math
from collections import namedtuple
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import os

Node = namedtuple("Node", ['index', 'demand', 'x', 'y'])
nodes = []

class CVRPORtools:

	def __init__(self, v, m, Q):
		self._v = v
		self._m = m
		self._Q = Q

	def parse_input_matrix(self, input_file):
		input_data = ''.join(input_file.readlines())

		# parse the input
		lines = input_data.split('\n')

		for i in range(0, self._v):
			line = lines[i]
			parts = line.split()
			""" Set all demands to 1 """
			nodes.append(Node(i, float(parts[3]), float(parts[1]), float(parts[2])))

	def solve(self):
		"""parameters"""
		routing = pywrapcp.RoutingModel(self._v, self._m)
		search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
		# Setting first solution heuristic (cheapest addition).
		search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
		#search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.SIMULATED_ANNEALING)


		"""Travel cost"""
		routing.SetCost(length)
		"""Set Depot"""
		routing.SetDepot(0)
		""" demands"""
		demands = []
		for i in range(0, self._v):
			demands.append(int(nodes[i][1]))
		print demands
		routing.AddVectorDimension(demands, self._Q, True, "Demand")

		"""SOLVE!"""
		assignment = routing.SolveWithParameters(search_parameters)
		##    print assignment

		if assignment:
			Objective = assignment.ObjectiveValue()
			print "obj:", assignment.ObjectiveValue()
			# Inspect solution.
			print "routing.vehicles:", routing.vehicles()
			routes = []
			for i in range(0, routing.vehicles()):
				route_number = i
				routes.append([])
				node = routing.Start(route_number)
				route = []
				route.append(0)
				if routing.IsVehicleUsed(assignment, i):
					while True:
						node = assignment.Value(routing.NextVar(node))
						if not routing.IsEnd(node):
							route.append(int(node))
						else:
							break
				route.append(0)
				routes[route_number].append(route)
		else:
			print('No solution found.')

		obj = 0
		for v in range(0, self._m):
			vehicle_tour = routes[v][0]
			if len(vehicle_tour) > 0:
				for i in range(0, len(vehicle_tour) - 1):
					obj += length(int(vehicle_tour[i]), int(vehicle_tour[i + 1]))
		print "calculated obj", obj

		outputData = str(Objective) + ' ' + str(0) + '\n'
		for i in range(0, routing.vehicles()):
			for j in range(0, len(routes[i])):
				outputData += str(routes[i][j]) + ' '
			outputData += '\n'
		return outputData

def length( node1, node2):
		return math.sqrt((nodes[node1][2] - nodes[node2][2]) ** 2 +
						 (nodes[node1][3] - nodes[node2][3]) ** 2)


def main():
	myModel = CVRPORtools(80,10,100)
	input_data_file = open('./examples/python/data/augerat/n80.txt', 'r')
	myModel.parse_input_matrix(input_data_file)
	input_data_file.close()
	print myModel.solve()

if __name__ == '__main__':
	start = os.times()
	main()
	end = os.times()
	# user time, system time, children user time, children system time, and elapsed real time since a fixed point in the past
	print "Time taken: ", end[-1] - start[-1]