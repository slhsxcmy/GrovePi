Q4.1  
cd my-imaginary-repo  
touch my_second_file.py  
git add my_second_file.py  
git commit -m "message"  
git push  

Q4.2  
We wrote the code on VM first and pushed the code to github. We then used ssh to connect to RPi and pulled code to RPi. Next time, we can learn to make minor, efficient changes to the code on RPi natively with nano, emacs, or vim.  

Q4.3  
We digged through the grovepi.py file and found the function grovepi.ultrasonicRead(pin). It has this line of code: "time.sleep(.06)	#firmware has a time of 50ms so wait for more than that." The default delay is 60ms since the firmware has a time of 50ms. It is this sleep function that is causing the constant delay of 60ms. When it tries to read the ultrasonic ranger output using the `grovepi` python library, the Raspberry Pi uses I2C Protocol to communicate with the Atmega328P on the GrovePi.  
