#presence dependent light control

import time
import sqlite3
from tkinter import *
import matplotlib.pyplot as plt
import matplotlib
import paho.mqtt.client as mqtt
import datetime


# Connect the Grove Light Sensor to analog port A0
# SIG,NC,VCC,GND
light_sensor = 0
sensor_value = ''
topic_value = ''

#database
conn = sqlite3.connect('Database_sensor.db')
print('database created')
Lt= conn.cursor()

Lt.execute('CREATE TABLE IF NOT EXISTS Data(Datestmp TEXT,Topic TEXT,Sensor_Data TEXT )')

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global sensor_value
    global topic_value

    sensor_value = str(msg.payload)
    sense = 0x0F & sensor_value
    print('hi')
    topic_value = str(msg.topic)
    print(sensor_value)

    unix = int( time.time())
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    if topic_value== 'SmartCities/Temperature':
        Lt.execute("SELECT * FROM Data WHERE Topic ='SmartCities/Temperature' ORDER BY Datestmp DESC LIMIT 1")
        result = Lt.fetchone()
    elif topic_value== 'SmartCities/Humidity':
        Lt.execute("SELECT * FROM Data WHERE Topic ='SmartCities/Humididty' ORDER BY Datestmp DESC LIMIT 1")
        result = Lt.fetchone()
    elif topic_value== 'SmartCities/PeopleCount':
        Lt.execute("SELECT * FROM Data WHERE Topic ='SmartCities/PeopleCount' ORDER BY Datestmp DESC LIMIT 1")
        result = Lt.fetchone()
    elif topic_value== 'SmartCities/Motion':
        Lt.execute("SELECT * FROM Data WHERE Topic ='SmartCities/Motion' ORDER BY Datestmp DESC LIMIT 1")
        result = Lt.fetchone()
    elif topic_value== 'SmartCities/Light':
        Lt.execute("SELECT * FROM Data WHERE Topic ='SmartCities/Light' ORDER BY Datestmp DESC LIMIT 1")
        result = Lt.fetchone()
    else:
        result = None

    if result is None:
        Lt.execute("INSERT INTO Data(Datestmp,Topic,Sensor_Data)VALUES (?,?,?)",(date,topic_value,sensor_value))
    else:
        if( sensor_value != result[2]):
            print('inside',sensor_value)
            Lt.execute("INSERT INTO Data(Datestmp,Topic,Sensor_Data)VALUES (?,?,?)",(date,topic_value,sensor_value))
        else:
            print("repeated data")
    conn.commit()

    print(msg.topic+" "+str(msg.payload))
    print('hi')


    if msg.topic == "SmartCities/Temperature":
        sensor_value = msg.payload
        topic_value = msg.topic
        print(sensor_value)
        print("Received message #1, do something")
        # Do something


    if msg.payload == "World!":
        print("Received message #2, do something else")
        #Do something else



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("iot.eclipse.org", 1883, 60)
client.subscribe("SmartCities/#")
client.loop_forever()


Lt.close()
conn.close()



