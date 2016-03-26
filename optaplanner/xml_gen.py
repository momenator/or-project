from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from xml.dom import minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def sample_xml():
	top = Element('top')

	child = SubElement(top, 'child')
	child.text = 'This child contains text.'

	child_with_tail = SubElement(top, 'child_with_tail')
	child_with_tail.text = 'This child has regular text.'
	child_with_tail.tail = 'And "tail" text.'

	child_with_entity_ref = SubElement(top, 'child_with_entity_ref')
	child_with_entity_ref.text = 'This & that'

	print prettify(top)

def generate_cvrp(input_file, vehicle, vehicle_capacity):
	"""
		XML Structure:
		VrpVehicleRoutingSolution
			id
			name
			distanceType
			distanceUnitOfMeasurement
			locationList
				VrpAirLocation
					id
					latitude
					longitude
			depotList
				VrpDepot
					id
					location
			vehicleList
				VrpVehicle
					id
					capacity
					depot
			customerList
				VrpCustomer
					id
					location
					demand
	"""

	# some counters to track the id number and references
	id_counter = 1
	depot_id = 1
	location_id = []
	# can be replaced with an array if the nodes have different demands


	VrpVehicleRoutingSolution = Element('VrpVehicleRoutingSolution', id=str(id_counter))
	id_counter+=1

	rootId = SubElement(VrpVehicleRoutingSolution,'id')
	rootId.text = '0'

	rootName = SubElement(VrpVehicleRoutingSolution,'name')
	rootName.text = '60-node'

	rootDistanceType = SubElement(VrpVehicleRoutingSolution,'distanceType')
	rootDistanceType.text = 'AIR_DISTANCE'

	distanceUnitOfMeasurement = SubElement(VrpVehicleRoutingSolution, 'distanceUnitOfMeasurement')
	distanceUnitOfMeasurement.text = 'distance'

	# Locations
	locationList = SubElement(VrpVehicleRoutingSolution, 'locationList',id=str(id_counter))
	id_counter+=1

	for line in input_file: # range of input file....
		line = line.replace('\n', '')
		lineArgs = line.split(' ')

		VrpAirLocationElem = SubElement(locationList, 'VrpAirLocation', id=str(id_counter))

		VrpAirLocationElemId = SubElement(VrpAirLocationElem, 'id')
		VrpAirLocationElemId.text = str(lineArgs[0])

		VrpAirLocationElemLatitude = SubElement(VrpAirLocationElem, 'latitude')
		VrpAirLocationElemLatitude.text = str(lineArgs[1])

		VrpAirLocationElemLongitude = SubElement(VrpAirLocationElem, 'longitude')
		VrpAirLocationElemLongitude.text = str(lineArgs[2])

		if lineArgs[0] == '1':
			depot_id = id_counter

		if lineArgs[0] != '1':
			location_id.append(id_counter)

		id_counter+=1

	# Depot
	depotList = SubElement(VrpVehicleRoutingSolution, 'depotList',id=str(id_counter))
	id_counter += 1

	# Single depot
	VrpDepot = SubElement(depotList, 'VrpDepot',id=str(id_counter))
	VrpDepotId = SubElement(VrpDepot, 'id')
	VrpDepotId.text = '1'

	VrpDepotLocation = SubElement(VrpDepot, 'location', clas='VrpAirLocation', reference=str(depot_id))
	depot_id_2 = id_counter
	id_counter+=1

	# Vehicles
	vehicleList = SubElement(VrpVehicleRoutingSolution, 'vehicleList',id=str(id_counter))
	id_counter+=1

	# list of vehicles
	for i in range(1, vehicle + 1):
		VrpVehicleElem = SubElement(vehicleList, 'VrpVehicle',id=str(id_counter))
		VrpVehicleId = SubElement(VrpVehicleElem, 'id')
		VrpVehicleId.text = str(i)

		VrpVehicleCapacity = SubElement(VrpVehicleElem, 'capacity')
		VrpVehicleCapacity.text = str(vehicle_capacity)

		VrpVehicleDepot = SubElement(VrpVehicleElem, 'depot', reference=str(depot_id_2))

		id_counter += 1

	# Nodes
	customerList = SubElement(VrpVehicleRoutingSolution, 'customerList',id=str(id_counter))

	id_counter += 1

	# list of nodes/customers
	for i in location_id:
		VrpCustomerElem = SubElement(customerList, 'VrpCustomer',id=str(id_counter))
		VrpCustomerId = SubElement(VrpCustomerElem, 'id')
		VrpCustomerId.text = str(i)

		VrpCustomerLocation = SubElement(VrpCustomerElem, 'location', clas='VrpAirLocation', reference=str(i))

		VrpCustomerDemand = SubElement(VrpCustomerElem, 'demand')
		VrpCustomerDemand.text = '1'

		id_counter += 1

	return prettify(VrpVehicleRoutingSolution)

def generate_cvrptw(input_file, vehicle, vehicle_capacity):
	"""
		XML Structure:
		VrpVehicleRoutingSolution
			id
			name
			distanceType
			distanceUnitOfMeasurement
			locationList
				VrpAirLocation
					id
					latitude
					longitude
			depotList
				VrpDepot
					id
					location
			vehicleList
				VrpVehicle
					id
					capacity
					depot
			customerList
				VrpCustomer
					id
					location
					demand
	"""

	# some counters to track the id number and references
	id_counter = 1
	depot_id = 1
	location_id = []
	# can be replaced with an array if the nodes have different demands

	#time window variables
	hour = 3600
	start_time = 9 * hour # 9am
	end_time = 17 * hour # 9am
	service_duration = hour / 4 # 15 mins

	VrpTimeWindowedVehicleRoutingSolution = Element('VrpTimeWindowedVehicleRoutingSolution', id=str(id_counter))
	id_counter+=1

	rootId = SubElement(VrpTimeWindowedVehicleRoutingSolution,'id')
	rootId.text = '0'

	rootName = SubElement(VrpTimeWindowedVehicleRoutingSolution,'name')
	rootName.text = '227-node-cvrptw'

	rootDistanceType = SubElement(VrpTimeWindowedVehicleRoutingSolution,'distanceType')
	rootDistanceType.text = 'AIR_DISTANCE'

	distanceUnitOfMeasurement = SubElement(VrpTimeWindowedVehicleRoutingSolution, 'distanceUnitOfMeasurement')
	distanceUnitOfMeasurement.text = 'distance'

	# Locations
	locationList = SubElement(VrpTimeWindowedVehicleRoutingSolution, 'locationList',id=str(id_counter))
	id_counter+=1

	for line in input_file: # range of input file....
		line = line.replace('\n', '')
		lineArgs = line.split(' ')

		VrpAirLocationElem = SubElement(locationList, 'VrpAirLocation', id=str(id_counter))

		VrpAirLocationElemId = SubElement(VrpAirLocationElem, 'id')
		VrpAirLocationElemId.text = str(lineArgs[0])

		VrpAirLocationElemLatitude = SubElement(VrpAirLocationElem, 'latitude')
		VrpAirLocationElemLatitude.text = str(lineArgs[1])

		VrpAirLocationElemLongitude = SubElement(VrpAirLocationElem, 'longitude')
		VrpAirLocationElemLongitude.text = str(lineArgs[2])

		if lineArgs[0] == '1':
			depot_id = id_counter

		if lineArgs[0] != '1':
			location_id.append(id_counter)

		id_counter+=1

	# Depot
	depotList = SubElement(VrpTimeWindowedVehicleRoutingSolution, 'depotList',id=str(id_counter))
	id_counter += 1

	# Single depot
	VrpTimeWindowedDepot = SubElement(depotList, 'VrpTimeWindowedDepot',id=str(id_counter))
	VrpDepotId = SubElement(VrpTimeWindowedDepot, 'id')
	VrpDepotId.text = '1'

	VrpTimeWindowedDepotLocation = SubElement(VrpTimeWindowedDepot, 'location', clas='VrpAirLocation', reference=str(depot_id))
	VrpTimeWindowedDepotReadyTime = SubElement(VrpTimeWindowedDepot, 'readyTime')
	VrpTimeWindowedDepotReadyTime.text = str(start_time)
	VrpTimeWindowedDepotDueTime = SubElement(VrpTimeWindowedDepot,'dueTime')
	VrpTimeWindowedDepotDueTime.text = str(end_time)

	depot_id_2 = id_counter
	id_counter+=1

	# Vehicles
	vehicleList = SubElement(VrpTimeWindowedVehicleRoutingSolution, 'vehicleList',id=str(id_counter))
	id_counter+=1

	# list of vehicles
	for i in range(1, vehicle + 1):
		VrpVehicleElem = SubElement(vehicleList, 'VrpVehicle',id=str(id_counter))
		VrpVehicleId = SubElement(VrpVehicleElem, 'id')
		VrpVehicleId.text = str(i)

		VrpVehicleCapacity = SubElement(VrpVehicleElem, 'capacity')
		VrpVehicleCapacity.text = str(vehicle_capacity)

		VrpVehicleDepot = SubElement(VrpVehicleElem, 'depot', clas='VrpTimeWindowedDepot', reference=str(depot_id_2))

		id_counter += 1

	# Nodes
	customerList = SubElement(VrpTimeWindowedVehicleRoutingSolution, 'customerList',id=str(id_counter))

	id_counter += 1

	# list of nodes/customers
	for i in location_id:
		VrpTimeWindowedCustomerElem = SubElement(customerList, 'VrpTimeWindowedCustomer',id=str(id_counter))
		VrpTimeWindowedCustomerId = SubElement(VrpTimeWindowedCustomerElem, 'id')
		VrpTimeWindowedCustomerId.text = str(i)

		VrpTimeWindowedCustomerLocation = SubElement(VrpTimeWindowedCustomerElem, 'location', clas='VrpAirLocation', reference=str(i))

		VrpTimeWindowedCustomerDemand = SubElement(VrpTimeWindowedCustomerElem, 'demand')
		VrpTimeWindowedCustomerDemand.text = '1'

		VrpTimeWindowedCustomerReadyTime = SubElement(VrpTimeWindowedCustomerElem, 'readyTime');
		VrpTimeWindowedCustomerReadyTime.text = str(start_time)

		VrpTimeWindowedCustomerDueTime = SubElement(VrpTimeWindowedCustomerElem, 'dueTime');
		VrpTimeWindowedCustomerDueTime.text = str(end_time)

		VrpTimeWindowedCustomerServiceDuration = SubElement(VrpTimeWindowedCustomerElem, 'serviceDuration');
		VrpTimeWindowedCustomerServiceDuration.text = str(service_duration)

		id_counter += 1

	return prettify(VrpTimeWindowedVehicleRoutingSolution)

if __name__ == '__main__':
	input_data_file = open('../dataset/cvrp_60.txt', 'r')
	res = generate_cvrp(input_data_file, 5, 15)
	res_xml = open('./res.xml', "w")
	res_xml.write(res)