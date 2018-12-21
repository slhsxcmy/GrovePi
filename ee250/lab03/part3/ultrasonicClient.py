import socket
def UltrasonicClient():
	host = '192.168.0.201'
	port = 5000
	# server_addr = '192.168.0.153' # Mingyu
	server_addr = '192.168.0.92' # Jui Po
	dst_port = 8050
	ultrasonic_ranger = 4

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
	s.bind((host,port))

	
	print("Client at " + host + " started. ")
	print("Sending from Port " + str(port) + ". ")
	print("To Port " + str(dst_port) + " at " + server_addr + ". ")

	while True:
		server = (server_addr, int(dst_port))
		message = str(grovepi.ultrasonicRead(ultrasonic_ranger)) + " cm"
		s.sendto(message.encode('utf-8'), server) 
		print("RPi: " + message)
		time.sleep(0.2)
	s.close()


# Ultrasonic Sensor Client
# 
# This code runs on the Raspberry Pi. It should sit in a loop which reads from
# the Grove Ultrasonic Ranger and sends the reading to the Ultrasonic Sensor 
# Server running on your VM via UDP packets. 

import sys
# By appending the folder of all the GrovePi libraries to the system path here,
# we are able to successfully `import grovepi`
sys.path.append('../../../Software/Python/')
import time
import grovepi

if __name__ == '__main__':
    UltrasonicClient()
