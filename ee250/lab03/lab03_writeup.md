Question 1: Copy-paste the output you see when running both files into your lab03_writeup.md   
text file. Make sure we can distinguish between the two outputs in your writeup.   
What happens when you try to run   both server scripts? Explain what you see and why this is happening.   
Answer:  
Traceback (most recent call last):  
	File "udpServer2.py", line 30, in <module>  
		Process2()  
	File "udpServer2.py", line 16, in Process2  
		s.bind((host,port))  
OSError: [Errno 48] Address already in use  
The error occur because we tried to connect two sockets to the same port (5000)  
  
Question 2: Open a third terminal and run the client script (`python3 udpClient.py`).   
Make sure not to run this with sudo rights! Copy-paste the output you see after running `udpClient.py`  
into your lab writeup. Then, change the `port` variable to 1024, and run the script again.   
Explain in detail what outputs you see and why you are seeing it.  
Answer:  
Traceback (most recent call last):  
	File "udpClient.py", line 33, in <module>  
		Main()  
	File "udpClient.py", line 13, in Main  
		s.bind((host,port))  
PermissionError: [Errno 13] Permission denied  
The error occur because we tried to use port 1023 for the client. Ports 0 - 1023 are reserved  
for core protocols. Ports 1024 and 5001 are free for use so the client program runs when port   
of the client is changed to 1024 or 5001.  

Question 3: In your answer sheet, list out the private IPv4 addresses of both your VM and rpi.  
Also, indicate which virtual machine manager you use (i.e. VirtualBox, VMware Fusion Pro,  
VMware Workstation).  
Private IPv4 address of VirtualBox VM: 10.0.2.15  
Private IPv4 address of Raspberry Pi : 192.168.0.201   
Private IPv4 address of Host OS      : 192.168.0.153   
