import json
import serial
import sys, time, datetime
import gmplot 	

PY_UART_SERIAL = "/dev/ttyAMA0"
OLI_MAC_SERIAL = "/dev/tty.usbserial-DN02T3GA"
BAUDRATE = 9600

class NodeHub():
	def __init__(self):
		self.serial = None
		self.nodeLocations = {}
		self.plotter = None

	# decodes data from xbee from json
	def parse_recv_data(self, data):
		return json.loads(data)

	# encodes data for xbee to json
	def encode_send_data(self, data):
		return json.dumps(data)

	# TODO figure out what to send if we want to send anything
	def build_send_data(self):
		pass

	def handle_recv_data(self, data):
		if data["latitude"] is not None and data["longitude"] is not None and data["altitude"] is not None:
			self.nodeLocations[data["node"]] = {'latitude': data["latitude"], 
												'longitude': data["longitude"],
												'altitude': data["altitude"]}
			print("node: {}\t\tlocation: {}, {}\t\taltitude: {}".format(data["node"], data["latitude"], data["longitude"], data["altitude"]))
		else:
			print("node: {} data is none".format(data["node"]))

	def connect_xbee(self):
		# connect to xbee over serial 
		self.serial = serial.Serial(OLI_MAC_SERIAL, BAUDRATE, timeout = 20)

	def init_gmplotter(self):
		self.plotter = gmplot.GoogleMapPlotter(42.3398, -71.0892, 16)

	def plot_points(self):
		for node in self.nodeLocations:
			color = self.get_node_color(node)
			lat = [self.nodeLocations[node]["latitude"]]
			lng = [self.nodeLocations[node]["longitude"]]
			self.plotter.scatter(lat, lng, color, marker=True)

		self.plotter.draw('node_locations.html')

	def get_node_color(self, node):
		# colors correspond to leds on node
		if node == '1':
			return 'r'
		elif node == '2':
			return 'g'
		elif node == '3':
			return 'b'
		else:
			return 'y'

	def get_data(self, plotMap):
		while True:
			recv_data = self.serial.readline()
			if recv_data:
				recv_data = recv_data.strip('\n')
				try:
					processed_data = self.parse_recv_data(recv_data)
					self.handle_recv_data(processed_data)
				except:
					print("invalid json data")
					continue
			else:
				print("no data received")

			if plotMap:
				self.init_gmplotter()
				self.plot_points()


	def close(self):
		self.serial.close()


	

