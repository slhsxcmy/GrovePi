import socket

def LEDClient():
	host = '192.168.0.201'
	port = 5000

	s = socket.socket() 
	s.connect((host,port))

	print("Client connected to " + host + " on Port " + str(port) + ". ")
	
	while True:
		message = input("-> ")
		s.send(message.encode('utf-8')) 
		message = s.recv(1024).decode('utf-8') 
		print("Received from server: " + message)
	s.close()

# LED Client 
#
# This code runs on yoru VM and sends requests to the Raspberry Pi to turn on 
# and off the Grove LED using TCP packets.

if __name__ == '__main__':
	LEDClient()