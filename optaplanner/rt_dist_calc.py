import numpy as np
import xml.etree.ElementTree as ElementTree


def extract_routes(input_file):
	routes = {}
	tree = ElementTree.parse(input_file)
	root = tree.getroot()
	curVehicle = 1

	for rt in root.iter('vehicleList'):
		for leg in rt.iter('VrpVehicle'):
			routes[curVehicle] = []
			for leg2 in leg.iter('nextCustomer'):
				curNodeId = leg2.find('id').text
				routes[curVehicle].append(int(curNodeId) - 2) # diff between id in xml and real id in raw dataset
				#print leg2.attrib
			curVehicle += 1

	return routes

def parse_coordinates_matrix(infile):
	coordinatesDict = {}

	for line in infile:
		line.replace("\n","")
		lineArg = line.split(" ")
		coordinatesDict[int(lineArg[0])] = {'x':float(lineArg[1]) ,'y':float(lineArg[2])}
	return coordinatesDict


def get_total_distance(ref_file, routes):
	# distance in km
	total_dist = 0
	coordinatesDict = parse_coordinates_matrix(ref_file)
	for route in routes:
		# this is the current route
		for i in range(1, len(routes[route])):
			curNode = routes[route][i-1]
			nextNode = routes[route][i]
			curDist = haversine(coordinatesDict[curNode]['x'],coordinatesDict[curNode]['y'],
								coordinatesDict[nextNode]['x'], coordinatesDict[nextNode]['y'])
			total_dist += curDist
		# add distance from depot to first node and last node to depot
		first_last_leg = haversine(coordinatesDict[1]['x'], coordinatesDict[1]['y'],
								   coordinatesDict[routes[route][0]]['x'], coordinatesDict[routes[route][0]]['y']) + \
						 haversine(coordinatesDict[1]['x'], coordinatesDict[1]['y'],
								   coordinatesDict[routes[route][-1]]['x'], coordinatesDict[routes[route][-1]]['y'])
		total_dist += first_last_leg

	return total_dist

def haversine(lon1, lat1, lon2, lat2):
	"""
	Calculate the great circle distance between two points
	on the earth specified in decimal degrees of latitude and longitude.
	https://en.wikipedia.org/wiki/Haversine_formula
	Args:
		lon1: longitude of pt 1,
		lat1: latitude of pt 1,
		lon2: longitude of pt 2,
		lat2: latitude of pt 2
	Returns:
		the distace in km between pt1 and pt2
	"""
	# convert decimal degrees to radians
	lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

	# haversine formula
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = (np.sin(dlat / 2) ** 2 + np.cos(lat1) *
		 np.cos(lat2) * np.sin(dlon / 2) ** 2)
	c = 2 * np.arcsin(np.sqrt(a))

	# 6367 km is the radius of the Earth
	km = 6367 * c
	return km

def main():
	in_file = open('./cvrptw-227customers-solved.xml')
	res = extract_routes(in_file)
	ref_file = open('../dataset/nodes_coordinates.txt')
	print 'The total distance is', round(get_total_distance(ref_file,res),2)

if __name__ == "__main__":
	#here
	main()