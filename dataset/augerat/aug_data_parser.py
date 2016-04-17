import numpy as np
import xml.etree.ElementTree as ElementTree

def parse_data(infile):
	tree = ElementTree.parse(infile)
	root = tree.getroot()
	"""
		nodes = {
			1: {
				coordinates:{
					x: 23,
					y: 67
				},
				demand : 45
			}
			...
		}
	"""
	nodes = {}

	for rt in root.iter('node'):
		curNode =  rt.attrib['id']

		nodes[curNode] = {}
		nodes[curNode]['coordinates'] = {}
		for cx in rt.iter('cx'):
			nodes[curNode]['coordinates']['x'] = cx.text
		for cy in rt.iter('cy'):
			nodes[curNode]['coordinates']['y'] = cy.text

	for rt in root.iter('request'):
		curNode = rt.attrib['node']

		for dm in rt.iter('quantity'):
			nodes[curNode]['demand'] = dm.text

	nodes['1']['demand'] = False

	return nodes

def main():
	in_file = open('./A-n80-k10.xml')
	test_data =  parse_data(in_file)
	num_node = 80
	ref_file = open('./A-n80-k10-parsed.txt', "w")

	for i in range(1, num_node + 1):
		# node x y demand
		ref_file.write(str(i)+ " " + str(test_data[str(i)]['coordinates']['x'])
					   + " " + str(test_data[str(i)]['coordinates']['y'])
					   + " " +  str(test_data[str(i)]['demand']) + "\n" )

	print "done"

if __name__ == "__main__":
	#here
	main()