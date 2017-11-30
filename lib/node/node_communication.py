import json
import serial
import sys, time, datetime 	

UART_SERIAL_PORT = "/dev/ttyAMA0"
OLI_MAC_SERIAL = "/dev/tty.usbserial-DN02T3GA"
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
		print("lat: " + data["latitutde"])
		print("lon: " + data["longitude"])
		print("alt: " + data["altitude"])

	def connect_xbee(self):
		# connect to xbee over serial 
		# TODO define timeout better to match node xbees
		self.serial = serial.Serial(OLI_MAC_SERIAL, BAUDRATE, timeout = 10)

	def get_data(self):
		while True:
			recv_data = serial_connection.readline()

			if recv_data is not None:
				print("received data")
				recv_data = recv_data.strip('\n')
				processed_data = self.parse_recv_data(recv_data)
				self.handle_recv_data(processed_data)
			else:
				print("no data received")

	def close(self):
		self.serial.close()


	

