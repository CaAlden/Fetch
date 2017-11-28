import json
import serial
import sys, time, datetime 	
import gps_util	


SERIAL_PORT = “/dev/ttyAMA0”
BAUDRATE = 9600

class NodeHub():
	def __init__(self):
		self.serial = None

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
		print("node: " + data["node"])
		print("gps: " + data["gps"])
		coord = gps_util.GPSCoord.from_GPGLL_string(data["gps"])
		print("lat: " + str(coord.latitutde))
		print("lon: " + str(coord.longitude))

	def connect_xbee(self):
		# connect to xbee over serial 
		# TODO define timeout better to match node xbees
		self.serial = serial.Serial(SERIAL_PORT, BAUDRATE, timeout = 10)

	def get_data(self):
		while True:
			recv_data = serial_connection.readline()

			if recv_data is not None:
				recv_data = recv_data.strip('\n')
				processed_data = self.parse_recv_data(recv_data)
				self.handle_recv_data(processed_data)

	def close(self):
		self.serial.close()


	

