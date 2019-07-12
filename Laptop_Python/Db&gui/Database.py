#Database file

import time
import sqlite3
from tkinter import *
import matplotlib.pyplot as plt
import matplotlib
import paho.mqtt.client as mqtt
import datetime

myhost = "raspberrypig25"

light_sensor = 0
sensor_value = ''
topic_value = ''

#create database
conn = sqlite3.connect('Database_SmartLib_Group25.db')
print('database created')
Lt= conn.cursor() # a cursor for the database

Lt.execute('CREATE TABLE IF NOT EXISTS Data(Datestmp TEXT,Topic TEXT,Sensor_Data TEXT )') # creating a table

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    global sensor_value
    global topic_value

    sensor_value = msg.payload.decode('utf-8')
    topic_value = msg.topic
    #.decode('utf-8')

    unix = int( time.time()) #exract the current time when the data is received via mqtt
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S')) #write down in the format of year, month, day gours, minute, second
    
    #Obtain the existing data for every topic to prevent overwriting the data into the database
    if topic_value== 'SmartCities/INpeoplecount':
        Lt.execute("SELECT * FROM Data WHERE Topic ='SmartCities/INpeoplecount' ORDER BY Datestmp DESC LIMIT 1")
        result = Lt.fetchone()
    elif topic_value== 'SmartCities/OUTpeoplecount':
        Lt.execute("SELECT * FROM Data WHERE Topic ='SmartCities/OUTpeoplecount' ORDER BY Datestmp DESC LIMIT 1")
        result = Lt.fetchone()
    elif topic_value== 'SmartCities/peoplecount':
        Lt.execute("SELECT * FROM Data WHERE Topic ='SmartCities/peoplecount' ORDER BY Datestmp DESC LIMIT 1")
        result = Lt.fetchone()
    elif topic_value== 'SmartCities/Temperature':
        Lt.execute("SELECT * FROM Data WHERE Topic ='SmartCities/Temperature' ORDER BY Datestmp DESC LIMIT 1")
        result = Lt.fetchone()
    elif topic_value== 'SmartCities/TargetTemperature':
        Lt.execute("SELECT * FROM Data WHERE Topic ='SmartCities/TargetTemperature' ORDER BY Datestmp DESC LIMIT 1")
        result = Lt.fetchone()
    elif topic_value== 'SmartCities/LightIntensity':
        Lt.execute("SELECT * FROM Data WHERE Topic ='SmartCities/LightIntensity' ORDER BY Datestmp DESC LIMIT 1")
        result = Lt.fetchone()
    elif topic_value== 'SmartCities/MotionDetected':
        Lt.execute("SELECT * FROM Data WHERE Topic ='SmartCities/MotionDetected' ORDER BY Datestmp DESC LIMIT 1")
        result = Lt.fetchone()
    elif topic_value== 'SmartCities/WeatherForecast':
        Lt.execute("SELECT * FROM Data WHERE Topic ='SmartCities/WeatherForecast' ORDER BY Datestmp DESC LIMIT 1")
        result = Lt.fetchone()
    elif topic_value== 'Database/Heater':
        Lt.execute("SELECT * FROM Data WHERE Topic ='Database/Heater' ORDER BY Datestmp DESC LIMIT 1")
        result = Lt.fetchone()
    elif topic_value== 'Database/Cooler':
        Lt.execute("SELECT * FROM Data WHERE Topic ='Database/Cooler' ORDER BY Datestmp DESC LIMIT 1")
        result = Lt.fetchone()
    elif topic_value== 'Database/RedLed':
        Lt.execute("SELECT * FROM Data WHERE Topic ='Database/RedLed' ORDER BY Datestmp DESC LIMIT 1")
        result = Lt.fetchone()
    elif topic_value== 'Database/BlueLed':
        Lt.execute("SELECT * FROM Data WHERE Topic ='Database/BlueLed' ORDER BY Datestmp DESC LIMIT 1")
        result = Lt.fetchone()
    elif topic_value== 'Database/GreenLed':
        Lt.execute("SELECT * FROM Data WHERE Topic ='Database/GreenLed' ORDER BY Datestmp DESC LIMIT 1")
        result = Lt.fetchone()
    elif topic_value== 'Database/Buzzer':
        Lt.execute("SELECT * FROM Data WHERE Topic ='Database/Buzzer' ORDER BY Datestmp DESC LIMIT 1")
        result = Lt.fetchone()
    elif topic_value== 'SmartCities/Library_Status':
        Lt.execute("SELECT * FROM Data WHERE Topic ='SmartCities/Library_Status' ORDER BY Datestmp DESC LIMIT 1")
        result = Lt.fetchone()
    else:
        result = None

    # Database is empty
    if result is None:
        Lt.execute("INSERT INTO Data(Datestmp,Topic,Sensor_Data)VALUES (?,?,?)",(date,topic_value,sensor_value))
    else: # compare the current sensor value and the value already stored in database
        if( sensor_value != result[2]):
            print('inside',sensor_value)#insert data
            Lt.execute("INSERT INTO Data(Datestmp,Topic,Sensor_Data)VALUES (?,?,?)",(date,topic_value,sensor_value))
        else:
            print("repeated data")
    conn.commit()





client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("iot.eclipse.org", 1883, 60)
client.subscribe("SmartCities/#")
client.subscribe("Database/#")
client.loop_forever()


Lt.close()
conn.close()



