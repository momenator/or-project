"""
  This script probably doesn't work anyway...
"""
import math
from collections import namedtuple
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
from datetime import datetime, timedelta

TIME_HORIZON = 24 * 60 * 60

Node = namedtuple("Node", ['index', 'demand', 'x', 'y'])
nodes = []
timeDict = {}
# Time window constraints
earliest = []
latest = []

class CVRPORtools:

	def __init__(self, v, m, Q):
		self._v = v
		self._m = m
		self._Q = Q

	def parse_node_matrix(self, input_file):
		input_data = ''.join(input_file.readlines())

		# parse the input
		lines = input_data.split('\n')

		for i in range(0, self._v):
			line = lines[i]
			parts = line.split()
			""" Set all demands to 1 """
			nodes.append(Node(i, 1, float(parts[1]), float(parts[2])))

	def parse_time_matrix(self, input_file):

		for line in input_file:
			line = line.replace("\n","")
			lineArg = line.split(" ")
			timeDict[(int(lineArg[0]), int(lineArg[1]))] = int(lineArg[2])

	def solve(self):
		"""parameters"""
		routing = pywrapcp.RoutingModel(self._v, self._m)
		search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
		# Setting first solution heuristic (cheapest addition).
		search_parameters.first_solution_strategy = \
			(routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

		"""Travel cost"""
		routing.SetCost(length)

		"""Set Depot"""
		routing.SetDepot(0)

		""" demands"""
		demands = []
		for i in range(0, self._v):
			demands.append(nodes[i][1])
		print demands
		routing.AddVectorDimension(demands, self._Q, True, "Demand")

		""" time windows """
		# add time window constraints here...
		# Add a dimension for time and a limit on the total time_horizon

		time_window = 8 * 60 ** 2 # 8 hours in secs
		start_time = 9 * 60 ** 2 # 9 am in secs
		end_time = start_time + time_window
		routing.AddDimension(time_length,
						 TIME_HORIZON,
						 TIME_HORIZON,
						 True,
						 "Time")

		time_dimension = routing.GetDimensionOrDie("Time")
		print "-- here --"
		print start_time
		print timedelta(0,start_time).seconds

		for curNode in nodes:
			time_dimension.CumulVar(int(curNode.index)).SetRange(
				timedelta(0,start_time).seconds,
				timedelta(0,end_time).seconds)

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

def length(node1, node2):
	return math.sqrt((nodes[node1][2] - nodes[node2][2]) ** 2 +
						 (nodes[node1][3] - nodes[node2][3]) ** 2)

def time_length(node1, node2):
	# grab the time duration from the travel (time) matrix
	#return timeDict[node1, node2]
	return length(node1,node2) * 20 * 60

def main():
	myModel = CVRPORtools(9, 3, 4)
	input_data_file = open('./examples/python/data/T-VRP-9.txt', 'r')
	#input_time_data_file = open()
	myModel.parse_node_matrix(input_data_file)
	input_data_file.close()
	print myModel.solve()

if __name__ == '__main__':
	main()