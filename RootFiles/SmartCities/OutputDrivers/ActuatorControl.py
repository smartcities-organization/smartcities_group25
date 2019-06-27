# This file controls all the output devices and also updates the data base on every major change 

import paho.mqtt.publish as publish
from grovepi import *
import time
import schedule
from plugwise.api import*
from datetime import datetime
import paho.mqtt.client as mqtt


##
RedLed =6
BlueLed =5
GreenLed =7

pinMode(RedLed,"OUTPUT")
pinMode(BlueLed,"OUTPUT")
pinMode(GreenLed,"OUTPUT")


DEFAULT_PORT ="/dev/ttyUSB0"
mac1="000D6F000278F2F3"
mac2="000D6F0002C0EB54"
stick = Stick(DEFAULT_PORT)
circle1 = Circle (mac1, stick)
circle2 = Circle (mac2, stick)

circle1.switch_off()
circle2.switch_off()
time.sleep(2)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    msg.payload = msg.payload.decode("utf-8")

    if msg.payload == "circle1_on":
        print("Switching ON Circle 1")
        circle1.switch_on ()
        publish.single("Database/Circle1", "1", hostname="test.mosquitto.org")

    if msg.payload == "circle1_off":
    	print("Switching OFF Circle 1")
    	circle1.switch_off ()
    	publish.single("Database/Circle1", "0", hostname="test.mosquitto.org")

    if msg.payload == "circle2_on":
        print("Switching ON Circle 2")
        circle2.switch_on ()
        publish.single("Database/Circle2", "1", hostname="test.mosquitto.org")

    if msg.payload == "circle2_off":
    	print("Switching OFF Circle 2")
    	circle2.switch_off ()
    	publish.single("Database/Circle2", "0", hostname="test.mosquitto.org")

    if msg.payload == "RedLedON":
        print("Red Led ON")
        digitalWrite(RedLed,1)
        publish.single("Database/RedLed", "1", hostname="test.mosquitto.org")

    if msg.payload == "RedLedOFF":
        print("Red Led OFF")
        digitalWrite(RedLed,0)
        publish.single("Database/RedLed", "0", hostname="test.mosquitto.org")

    if msg.payload == "BlueLedON":
        print("Blue Led ON")
        digitalWrite(BlueLed,1)
        publish.single("Database/BlueLed", "1", hostname="test.mosquitto.org")

    if msg.payload == "BlueLedOFF":
    	print("Blue Led OFF")
    	digitalWrite(BlueLed,0)
    	publish.single("Database/BlueLed", "0", hostname="test.mosquitto.org")

    if msg.payload == "GreenLedON":
        print("Green Led ON")
        digitalWrite(GreenLed,1)
        publish.single("Database/GreenLed", "1", hostname="test.mosquitto.org")

    if msg.payload == "GreenLedOFF":
        print("Green Led OFF")
        digitalWrite(GreenLed,0)
        publish.single("Database/GreenLed", "0", hostname="test.mosquitto.org")



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect("test.mosquitto.org", 1883, 60)
client.subscribe("SmartCities/#")
client.loop_forever()
