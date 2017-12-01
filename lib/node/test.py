import node_communication
import serial
import sys


print('connecting to xbee')
nodeHub = node_communication.NodeHub()
nodeHub.connect_xbee()

#print('init mapper')
#nodeHub.init_gmplotter()

print('reading from xbee')
nodeHub.get_data(True)

print('closing connection')
nodeHub.close()



