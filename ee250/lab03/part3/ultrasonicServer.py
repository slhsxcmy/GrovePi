import socket
def UltrasonicServer():
	host = '10.0.2.15'
	port = 9000

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((host,port))

	print("Server at " + host + " started. Listening on Port " + str(port) + ". ")
	while True:
		message, addr = s.recvfrom(1024)
		message = message.decode('utf-8')
		print("VM: " + message)
	s.close()

#Ultrasonic Sensor Server
#
# This code runs on your VM and receives a stream of packets holding ultrasonic
# sensor data and prints it to stdout. Use a UDP socket here.

if __name__ == '__main__':
	UltrasonicServer()