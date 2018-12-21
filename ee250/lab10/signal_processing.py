"""EE 250L Lab 10 Signal Processing

This file is the starter code for the lab assignment.

TODO: List team members here.
Mingyu Cui
Jui Po Hung

TODO: Insert Github repository link here.
git@github.com:usc-ee250-fall2018/signalproc-lab10-robert_nb.git
"""

import paho.mqtt.client as mqtt
import time
import requests
import json
from datetime import datetime


# MQTT variables
broker_hostname = "eclipse.usc.edu"
broker_port = 11000

#uncomment these lines to subscribe to real-time published data
ultrasonic_ranger1_topic = "ultrasonic_ranger1/real_data"
ultrasonic_ranger2_topic = "ultrasonic_ranger2/real_data"

#uncomment these lines to subscribe to recorded data being played back in a loop
# ultrasonic_ranger1_topic = "ultrasonic_ranger1/fake_data"
# ultrasonic_ranger2_topic = "ultrasonic_ranger2/fake_data"

# Lists holding the ultrasonic ranger sensor distance readings. Change the 
# value of MAX_LIST_LENGTH depending on how many distance samples you would 
# like to keep at any point in time.
# MAX_LIST_LENGTH = 100
MAX_LIST_LENGTH = 8
ranger1_dist = []
ranger2_dist = []

ranger1_movingAverage = []
ranger2_movingAverage = []

CUTOFF = 160
result = ""

def ranger1_callback(client, userdata, msg):
# 	# negative or too far -> invalid data
# 	if int(msg.payload) < 0 or int(msg.payload) > CUTOFF:
# 		return
	global ranger1_dist
	ranger1_dist.append(int(msg.payload))
	#truncate list to only have the last MAX_LIST_LENGTH values
	ranger1_dist = ranger1_dist[-MAX_LIST_LENGTH:]

def ranger2_callback(client, userdata, msg):
# 	# negative or too far -> invalid data
# 	if int(msg.payload) < 0 or int(msg.payload) > CUTOFF:
# 		return
	global ranger2_dist
	ranger2_dist.append(int(msg.payload))
	#truncate list to only have the last MAX_LIST_LENGTH values
	ranger2_dist = ranger2_dist[-MAX_LIST_LENGTH:]

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
	client.subscribe(ultrasonic_ranger1_topic)
	client.message_callback_add(ultrasonic_ranger1_topic, ranger1_callback)
	client.subscribe(ultrasonic_ranger2_topic)
	client.message_callback_add(ultrasonic_ranger2_topic, ranger2_callback)

# The callback for when a PUBLISH message is received from the server.
# This should not be called.
def on_message(client, userdata, msg): 
	print(msg.topic + " " + str(msg.payload))

def detectMovement():
	global ranger1_movingAverage
	global ranger2_movingAverage
	global result
	ranger1_movingAverageDiff = []
	ranger2_movingAverageDiff = []
	
	if len(ranger1_dist) > 0:
		ranger1_movingAverage.append(sum(ranger1_dist)/len(ranger1_dist))
		ranger1_movingAverage = ranger1_movingAverage[-MAX_LIST_LENGTH:]
	if len(ranger2_dist) > 0:
		ranger2_movingAverage.append(sum(ranger2_dist)/len(ranger2_dist))
		ranger2_movingAverage = ranger2_movingAverage[-MAX_LIST_LENGTH:]

	for i in range(1, len(ranger1_movingAverage)):
		ranger1_movingAverageDiff.append(ranger1_movingAverage[i] - ranger1_movingAverage[i-1])
	for i in range(1, len(ranger2_movingAverage)):
		ranger2_movingAverageDiff.append(ranger2_movingAverage[i] - ranger2_movingAverage[i-1])

	movement1 = sum(ranger1_movingAverageDiff)
	movement2 = sum(ranger2_movingAverageDiff)
	length1 = len((ranger1_movingAverageDiff))
	length2 = len((ranger2_movingAverageDiff))
	# print("movement1: " + str(ranger1_movingAverageDiff))
	# print("movement2: " + str(ranger2_movingAverageDiff))

	if(movement1 <= 5* length1 and movement1 >= -5* length1 and sum(ranger1_movingAverage) < CUTOFF*(length1+1)):
		result = "Still - Left"
	elif(movement2 <= 5* length2 and movement2 >= -5* length2 and sum(ranger2_movingAverage) < CUTOFF*(length2+1)):
		result = "Still - Right"
	elif(movement1 > 5* length1 and movement2 < -5* length2):
		result = "Moving Right"
	elif(movement2 > 5* length2 and movement1 < -5* length1):
		result = "Moving Left"
	else:
		result = "Nobody is Here"
	print(result)

if __name__ == '__main__':
	
	# This header sets the HTTP request's mimetype to `application/json`. This
    # means the payload of the HTTP message will be formatted as a json ojbect
    hdr = {
        'Content-Type': 'application/json',
        'Authorization': None #not using HTTP secure
    }
    # Connect to broker and start loop    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_hostname, broker_port, 60)
    client.loop_start()

    while True:
        """ You have two lists, ranger1_dist and ranger2_dist, which hold a window
        of the past MAX_LIST_LENGTH samples published by ultrasonic ranger 1
        and 2, respectively. The signals are published roughly at intervals of
        200ms, or 5 samples/second (5 Hz). The values published are the 
        distances in centimeters to the closest object. The measurements can
        technically take values up to 1024, but you will mainly see values 
        between 0-700. Jumps in values will most likely be from 
        inter-sensor-interference, so be sure to filter the signal accordingly
        to remove these jumps. 
        """
        
        # TODO: detect movement and/or position
        detectMovement()

        # The payload of our message starts as a simple dictionary. Before sending
        # the HTTP message, we will format this into a json object
        payload = {
            'time': str(datetime.now()),
            'event': str(result)
        }    

        print("ranger1: " + str(ranger1_dist[-1:]) + ", ranger2: " + 
                str(ranger2_dist[-1:])) 

        # Send an HTTP POST message and block until a response is given.
        # Note: requests() is NOT the same thing as request() under the flask 
        # library.
        response = requests.post("http://0.0.0.0:5000/post-event", headers = hdr,
                         data = json.dumps(payload))

        # Print the json object from the HTTP response
        print(response.json())

        
        time.sleep(0.2)

