"""EE 250L Lab 04 Starter Code

Run vm_subscriber.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("RPI_juipohun/ultrasonicRanger", 1)
    client.subscribe("RPI_juipohun/button", 1)
    client.message_callback_add("RPI_juipohun/ultrasonicRanger", on_message_ultra)
    client.message_callback_add("RPI_juipohun/button", on_message_button)
    #subscribe to the ultrasonic ranger topic here

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def on_message_ultra(client, userdata, msg):
    message = str(msg.payload, "utf-8")
    if not message:
        return
    else:
        print("VM: " + message)

def on_message_button(client, userdata, msg):
    message = str(msg.payload, "utf-8")
    if not message:
        return
    else:
        print(message)
if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        
        time.sleep(1)
            

