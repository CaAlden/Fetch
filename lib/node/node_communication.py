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

def connect_xbee():
	# connect to xbee over serial 
	serial_connection = serial.Serial(SERIAL_PORT, BAUDRATE)
	

