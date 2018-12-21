"""EE 250L Lab 04 Starter Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time
import sys
sys.path.append('../../../Software/Python/')
sys.path.append('../../Software/Python/grove_rgb_lcd')
import grove_rgb_lcd
import grovepi


pin_led = 3 #  LED on port D-3
pin_button = 2 # button on port D-2
grovepi.pinMode(pin_led,"OUTPUT")
grovepi.pinMode(pin_button,"INPUT")
ultrasonic_ranger = 4

grove_rgb_lcd.setRGB(0,0,255)

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("RPI_juipohun/led", 1)
    client.subscribe("RPI_juipohun/lcd", 1)
    client.message_callback_add("RPI_juipohun/led", on_message_led)
    client.message_callback_add("RPI_juipohun/lcd", on_message_lcd)
    #subscribe to topics of interest here

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def on_message_led(client, userdata, msg):
    message = str(msg.payload, "utf-8")
    if not message:
        return

    if message == 'LED_ON':
        grovepi.digitalWrite(pin_led,1)
        
        print('LED_ON Success')
    elif message == 'LED_OFF':
        grovepi.digitalWrite(pin_led,0)
        print('LED_OFF Success')
    else: 
        print('Command Not Recognized')
def on_message_lcd(client, userdata, msg):
    message = str(msg.payload, "utf-8")
    if not message:
        return
    else:
        grove_rgb_lcd.setText_norefresh(message)

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        message = str(grovepi.ultrasonicRead(ultrasonic_ranger)) + " cm"
        client.publish("RPI_juipohun/ultrasonicRanger",message, 1)
        if grovepi.digitalRead(pin_button) == 1:
            client.publish("RPI_juipohun/button", "Button pressed!", 1)

        time.sleep(1)
            

