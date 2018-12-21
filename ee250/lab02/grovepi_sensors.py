# THIS FILE IS FINAL

""" EE 250L Lab 02: GrovePi Sensors

List team members here.
Mingyu Cui
Jui Po Hung

Insert Github repository link here.
git@github.com:usc-ee250-fall2018/GrovePi-robert.git

Each team member should submit a copy of the team's code.
"""

"""python3 interpreters in Ubuntu (and other linux distros) will look in a 
default set of directories for modules when a program tries to `import` one. 
Examples of some default directories are (but not limited to):
  /usr/lib/python3.5
  /usr/local/lib/python3.5/dist-packages

The `sys` module, however, is a builtin that is written in and compiled in C for
performance. Because of this, you will not find this in the default directories.
"""

import sys
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('../../Software/Python/')
import grovepi
import time
import math

# This append is to support importing the LCD library.
sys.path.append('../../Software/Python/grove_rgb_lcd')
import grove_rgb_lcd

grove_rgb_lcd.setRGB(0,0,255) # set to blue so it looks better

"""
Grove Ultrasonic Ranger: D-4
Grove Rotary Angle Sensor: A-0
Grove LCD RGB Backlight: I2C-1
Grove Temperature & Humidity Sensor: D-5
"""


dht_sensor_port = 5 # connect the DHt sensor to port D-5
dht_sensor_type = 0 # use 0 for the blue-colored sensor and 1 for the white-colored sensor

ultrasonic_ranger = 4 # connect to port D-4

potentiometer = 0 # connect to port A-0
grovepi.pinMode(potentiometer,"INPUT")

"""This if-statement checks if you are running this python file directly. That 
is, if you run `python3 grovepi_sensors.py` in terminal, this if-statement will 
be true"""
if __name__ == '__main__':

	



	while True:
		try:
			#So we do not poll the sensors too quickly which may introduce noise,
			#sleep for a reasonable time of 1 second between each iteration.
			time.sleep(1)

			# Read value from range sensor
			ranger = grovepi.ultrasonicRead(ultrasonic_ranger)

			# Read value from potentiometer
			threshold = grovepi.analogRead(potentiometer)

#			print("threshold = %d ranger = %d" %(threshold, ranger))

			# compare ranger and threshold
			inbound = "           "

			if ranger <= threshold:
				inbound = "OBJ PRESENT"

			# get the temperature and Humidity from the DHT sensor
			[ temp,hum ] = grovepi.dht(dht_sensor_port,dht_sensor_type)
#			print("temp = %d humidity = %d%%" %(temp, hum))

			# check if we have nans
			# if so, then raise a type error exception
			if math.isnan(temp) is True or math.isnan(hum) is True:
				raise TypeError('nan error')

			# write all data to LCD
			grove_rgb_lcd.setText_norefresh("%4d %s\n%4dcm %3d%% %3dC" %(threshold, inbound, ranger, hum, temp))


		except TypeError as e:
			print(str(e))
		except KeyboardInterrupt:
			print ("KeyboardInterrupt")
			break
		except IOError:
			print ("IOError")
