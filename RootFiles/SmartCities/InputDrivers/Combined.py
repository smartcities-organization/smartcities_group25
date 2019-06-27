# people count publish file
# MQTT Publish Demo
# Publish two messages, to two different topics

import paho.mqtt.publish as publish
import grovepi
import math
import time
import schedule
from grove_rgb_lcd import *

setText("Welcome To \nSmart Library")
setRGB(0,128,64)


#publish.single("CoreElectronics/test", "Hello", hostname="test.mosquitto.org")
#publish.single("CoreElectronics/topic", "World!", hostname="test.mosquitto.org")


# Connect the Grove Ultrasonic Ranger to digital port D4
# SIG,NC,VCC,GND
ultrasonic_ranger = 3
dht_sensor_pin = 4
pir_sensor_pin = 8
lightsens_pin = 0

blue = 0    # The Blue colored sensor.
white = 1   # The White colored sensor.

lightsensor_thr = 10
distance =20
US_threshold =10
peoplecount =0
currentstate = False
previousstate = False

grovepi.pinMode(lightsens_pin,"INPUT")
grovepi.pinMode(pir_sensor_pin, "INPUT")

def CalcMotionDetection():
	if motion == 1:
		print("Motion detected")
	elif motion==0:
		print("No motion detected")
	else:
		print("ERROR.PIR")

def CalcPeopleCount():
	global previousstate
	global currentstate
	global peoplecount
	if distance < US_threshold :
			currentstate = True
	else:
		currentstate = False
	
	if currentstate != previousstate:
		if currentstate == True:
			peoplecount=peoplecount+1
			setText("People Count \n {}".format(str(peoplecount)))
			print("people count updated and published")
		previousstate = currentstate

def TempHum_job():
	[temp,humidity] = grovepi.dht(dht_sensor_pin,blue)
	if math.isnan(temp) == False and math.isnan(humidity) == False:
		if temp > 0:
			print("temp = %.02f C humidity =%.02f%%"%(temp, humidity))
			publish.single("SmartCities/Temperature", temp, hostname="test.mosquitto.org")
			publish.single("SmartCities/Humidity", humidity, hostname="test.mosquitto.org")
	else:
		print("nan values")
		#publish.single("SmartCities/Humidity", humidity, hostname="test.mosquitto.org")
		#publish.single("SmartCities/Temperature", temp, hostname="test.mosquitto.org") 

def LightIntensityCalc_job():
	Intensity = grovepi.analogRead(lightsens_pin)
	resistance = (float)((1023-Intensity)*10)/Intensity

	if resistance > lightsensor_thr:
		lux = 1
	elif resistance <= lightsensor_thr:
		lux = 0
	else:
		lux = -1
	print("Light Intensity is", resistance)
	print("Is the light above threshold =",lux)
	publish.single("SmartCities/LightIntensity", resistance, hostname="test.mosquitto.org")

def MotionDetection_job():
	publish.single("SmartCities/MotionDetected", motion, hostname="test.mosquitto.org")

def PeopleCount_job():
	publish.single("SmartCities/peoplecount", peoplecount, hostname="test.mosquitto.org")



#schedule.every(1).minute.at(":05").do(TempHum_job)
#schedule.every(1).minute.at(":10").do(LightIntensityCalc_job)
#schedule.every(1).minute.at(":15").do(PeopleCount_job)
schedule.every(5).seconds.do(MotionDetection_job)
schedule.every(5).seconds.do(PeopleCount_job)
schedule.every(5).seconds.do(TempHum_job)
schedule.every(5).seconds.do(LightIntensityCalc_job)

while True:
	try:
		#PIR Check
		motion=grovepi.digitalRead(pir_sensor_pin)
		CalcMotionDetection()
		
		# Read distance value from Ultrasonic and calculate people count 
		distance = grovepi.ultrasonicRead(ultrasonic_ranger)
		CalcPeopleCount()

		schedule.run_pending()
		time.sleep(.2)
	except TypeError:
        	print ("Error")
	except IOError:
        	print ("Error")
