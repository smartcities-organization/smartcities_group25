# the main Brain
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time
import schedule

myhostname = "iot.eclipse.org"

peopleIN =0
peopleOUT =0
peoplecount =0
SensorTemp = 0.0
LightIntensity = "LOW"
IsMotionDetected = 0
ForecastTemp1H =0.0

prev_peopleIN =0
prev_peopleOUT =0
prev_peoplecount =0
prev_SensorTemp = 0.0
prev_LightIntensity = "LOW"
prev_IsMotionDetected = 0
prev_ForecastTemp1H =0.0

calc = False
chgCheck = False

def changeCheck():
	init_passed = False


	global peopleIN 
	global peopleOUT 
	global peoplecount 
	global SensorTemp 
	global LightIntensity 
	global IsMotionDetected 
	global ForecastTemp1H 

	global prev_peopleIN 
	global prev_peopleOUT 
	global prev_peoplecount 
	global prev_SensorTemp 
	global prev_LightIntensity
	global prev_IsMotionDetected
	global prev_ForecastTemp1H


	if init_passed is True :

		if any ( [	prev_peopleIN != peopleIN, 
					prev_peopleOUT != peopleOUT,
					prev_peoplecount != peoplecount,
					prev_SensorTemp != SensorTemp,
					prev_LightIntensity != LightIntensity,
					prev_IsMotionDetected != IsMotionDetected,
					prev_ForecastTemp1H != ForecastTemp1H   ] ) :
			calc = True
	elif:
		prev_peopleIN = peopleIN
		prev_peopleOUT = peopleOUT
		prev_peoplecount = peoplecount
		prev_SensorTemp = SensorTemp
		prev_LightIntensity = LightIntensity
		prev_IsMotionDetected = IsMotionDetected
		prev_ForecastTemp1H = ForecastTemp1H

		init_passed = True




	prev_peopleIN = peopleIN
	prev_peopleOUT = peopleOUT
	prev_peoplecount = peoplecount
	prev_SensorTemp = SensorTemp
	prev_LightIntensity = LightIntensity
	prev_IsMotionDetected = IsMotionDetected
	prev_ForecastTemp1H = ForecastTemp1H



def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    msg.payload = msg.payload.decode("utf-8")
    global chgCheck
    chgCheck = True

    if msg.topic == "SmartCities/INpeoplecount":
    	global peopleIN
    	peopleIN = int(msg.payload)

    elif msg.topic == "SmartCities/OUTpeoplecount":
    	global peopleOUT
    	peopleOUT = int(msg.payload)

    elif msg.topic == "SmartCities/peoplecount":
    	global peoplecount
    	peoplecount = int(msg.payload)

    elif msg.topic == "SmartCities/Temperature":
    	global SensorTemp
    	SensorTemp = float(msg.payload)

    elif msg.topic == "SmartCities/LightIntensity":
    	global LightIntensity
    	LightIntensity = msg.payload

    elif msg.topic == "SmartCities/MotionDetected":
    	global IsMotionDetected
    	IsMotionDetected = int(msg.payload)

    elif msg.topic == "SmartCities/WeatherForecast":
    	global ForecastTemp1H
    	ForecastTemp1H = int(msg.payload)




client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(myhostname,1883,60)
client.subscribe("SmartCities/#")
client.loop_start()

while True:
	
	if chgCheck is True:

		changeCheck()
		
		if calc is True:
			print ("Calc in progress")
			# do the calculation
			calc = False

   		chgCheck = False
   


