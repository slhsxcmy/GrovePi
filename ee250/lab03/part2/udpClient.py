import socket

def Main():
	# Change the host and port as needed. For ports, use a number in the 9000 
	# range. 
	host = '192.168.0.201'
	# port = 1023 # permission denied, 1 - 1024 reserved
	port = 1024
	# port = 5001
	
	server_addr = '192.168.0.153'

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
	s.bind((host,port))

	# UDP is connectionless, so a client does not formally connect to a server
	# before sending a message.
	dst_port = input("destination port-> ")
	message = input("message-> ")
	while message != 'q':
		#tuples are immutable so we need to overwrite the last tuple
		server = (server_addr, int(dst_port))

		# for UDP, sendto() and recvfrom() are used instead
		s.sendto(message.encode('utf-8'), server) 
		data, addr = s.recvfrom(1024)
		data = data.decode('utf-8')
		print("Received from server: " + data)
		dst_port = input("destination port-> ")
		message = input("message-> ")
	s.close()

if __name__ == '__main__':
	Main()