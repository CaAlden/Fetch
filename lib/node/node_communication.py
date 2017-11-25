import json
import serial
import sys, time, datetime 		


SERIAL_PORT = “/dev/ttyAMA0”
BAUDRATE = 9600

# decodes data from xbee from json
def parse_recv_data(data):
	recv_data = json.loads(data)

# encodes data for xbee to json
def encode_send_data(data):
	return json.dumps(data)

# TODO figure out what to send if we want to send anything
def build_send_data():
	pass

# TODO define what this should do 
def handle_recv_data(data):
	pass

def connect_xbee():
	# connect to xbee over serial 
	# TODO define timeout better to match node xbees
	serial_connection = serial.Serial(SERIAL_PORT, BAUDRATE, timeout = 1)

	while True:
		recv_data = serial_connection.readline()

		if recv_data is not None:
			recv_data = recv_data.strip('\n')
			processed_data = parse_recv_data(recv_data)
			handle_recv_data(processed_data)

	serial_connection.close()

	

