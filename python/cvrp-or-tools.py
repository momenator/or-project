"""
  This script probably doesn't work anyway...
"""
import math
from collections import namedtuple
from ortools.constraint_solver import pywrapcp

customers = []

Customer = namedtuple("Customer", ['index', 'demand', 'x', 'y'])

def length(customer1, customer2):
    return round(math.sqrt((customers[customer1][2] - customers[customer2][2])**2 + (customers[customer1][3]- customers[customer2][3])**2),4)

def solve_it(input_data):
    # parse the input
    lines = input_data.split('\n')
    parts = lines[0].split()
    customer_count = int(parts[0])
    vehicle_count = int(parts[1])
    vehicle_capacity = int(parts[2])
    print "customer_count",customer_count
    print "vehicle_count", vehicle_count
    print "vehicle_capacity",vehicle_capacity
   
    for i in range(1, customer_count+1):
        line = lines[i]
        parts = line.split()
        customers.append(Customer(i-1, int(parts[0]), float(parts[1]), float(parts[2])))

    print ' ----------------------------------------------- Parameters ------------------------------------------------'
    routing = pywrapcp.RoutingModel(customer_count, vehicle_count)
    parameters = pywrapcp.RoutingSearchParameters()
    # Setting first solution heuristic (cheapest addition).
    parameters.first_solution = 'PathCheapestArc'
    # Disabling Large Neighborhood Search, comment out to activate it.
##    parameters.no_lns = True
    parameters.guided_local_search=True
    print ' ----------------------------------------------- Transport Cost ------------------------------------------------'
    routing.SetCost(length)
    routing.SetDepot(0)
    print ' ----------------------------------------------- Demand -------------------------------------'
    demands=[]
    for i in range(0, customer_count):
        demands.append(customers[i][1])
    routing.AddVectorDimension(demands,vehicle_capacity,1,"Demand")
    print ' ----------------------------------------------- Solve ------------------------------------------------'
    assignment = routing.Solve()
##    print assignment
    if assignment:
      Objective=assignment.ObjectiveValue()
      print "obj:", assignment.ObjectiveValue()
      print "strategy:",parameters.first_solution
      print "heuristic:",parameters.no_lns
      print "staus:",routing.status()

      # Inspect solution.
      print "routing.vehicles:",routing.vehicles()
      routes=[]
      for i in range(0,routing.vehicles()):
          route_number = i
          routes.append([])
          node = routing.Start(route_number)
          route=[]
          route.append(0) 
          if routing.IsVehicleUsed(assignment,i):
              while True:
                  node = assignment.Value(routing.NextVar(node))
                  if not routing.IsEnd(node):
                      route.append(int(node))
                  else :
                      break
          route.append(0)
          routes[route_number].append(route)
    else:
      print('No solution found.')

    obj = 0
    for v in range(0, vehicle_count):
        vehicle_tour = routes[v][0]
        if len(vehicle_tour) > 0:
            for i in range(0, len(vehicle_tour)-1):
                obj += round(length(int(vehicle_tour[i]),int(vehicle_tour[i+1])),0)
    print "calculated obj",obj

    outputData = str(Objective) + ' ' + str(0) + '\n'
    for i in range(0,routing.vehicles()):
        for j in range(0, len(routes[i])):
            outputData+=str(routes[i][j])+ ' '
        outputData += '\n'
    return outputData


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print 'Solving:', file_location
        print solve_it(input_data)
    else:

        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/vrp_5_4_1)'
