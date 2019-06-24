#presence dependent light control

import time
#import grovepi
import sqlite3
from tkinter import *
import matplotlib.pyplot as plt
import paho.mqtt.client as mqtt
import datetime


# Connect the Grove Light Sensor to analog port A0
# SIG,NC,VCC,GND
light_sensor = 0
sensor_value =""

# Connect the LED to digital port D4
# SIG,NC,VCC,GND
#led = 4

# Turn on LED once sensor exceeds threshold resistance
threshold = 10

#grovepi.pinMode(light_sensor,"INPUT")
#grovepi.pinMode(led,"OUTPUT")

#people count via mqtt
PeopleCount =1

#database
conn = sqlite3.connect('Light.db')
print('database created')
c= conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS LightData(datestmap TEXT,value TEXT)')

#GUI
root = Tk()
 
def plot():
    c.execute("SELECT datestmap, value FROM LightData")
    dates=[]
    values=[]
    for row in c.fetchall():
        dates.append(datetime.datetime.fromtimestamp(row[0]))
        values.append(row[1])
    plt.plot_light(dates,values)
    plt.show()



def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    


 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global sensor_value

    print(msg.topic+" "+str(msg.payload))

    if msg.topic == "SmartCities/sensor":
        sensor_value = msg.payload
        #print("Received message #1, do something")
        # Do something


    if msg.payload == "World!":
        print("Received message #2, do something else")
        # Do something else




button_1 = Button(root,text ='plot',command=plot)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect("test.mosquitto.org", 1883, 60)
client.subscribe("SmartCities/#")




while True:
    try:
        #if PeopleCount>=1:
        # Get sensor value
            #sensor_value = grovepi.analogRead(light_sensor)

            # Calculate resistance of sensor in K
            #resistance = (float)(1023 - sensor_value) * 10 / sensor_value

            #if resistance > threshold:
                # Send HIGH to switch on LED
            #    grovepi.digitalWrite(led,1)
            #else:
                # Send LOW to switch off LED
             #   grovepi.digitalWrite(led,0)

            #print("sensor_value = %d resistance = %.2f" %(sensor_value,  resistance))
        unix = int( time.time())
        date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
        c.execute("INSERT INTO LightData(datestmap,value)VALUES (?,?)",
        (date,sensor_value))
        conn.commit()
        time.sleep(2)

    except IOError:
        print ("Error")

    except KeyboardInterrupt:
        c.close()
        conn.close()