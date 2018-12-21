import socket

def LEDServer():
	host = '192.168.0.201'
	port = 5000
	led = 5 #  LED on port D-5
	grovepi.pinMode(led,"OUTPUT")

	s = socket.socket()
	s.bind((host,port))
	
	s.listen(1)
	print("Server at " + host + " started. Listening on Port " + str(port) + ". ")
	
	c, addr = s.accept()
	print("Connection from: " + str(addr))

	while True:
		message = c.recv(1024).decode('utf-8')
		if not message:
			break
		elif message == 'LED_ON':
			grovepi.digitalWrite(led,1)
			message = 'LED_ON Success'
			print("Sending: " + message)
			c.send(message.encode('utf-8'))
		elif message == 'LED_OFF':
			grovepi.digitalWrite(led,0)
			message = 'LED_OFF Success'
			print("Sending: " + message)
			c.send(message.encode('utf-8'))
		else:
			message = 'Command Not Recognized'
			print("Sending: " + message)
			c.send(message.encode('utf-8'))
	s.close()

# LED Server
# 
# This program runs on the Raspberry Pi and accepts requests to turn on and off
# the LED via TCP packets.

import sys
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('../../../Software/Python/')

import grovepi

if __name__ == '__main__':
	LEDServer()