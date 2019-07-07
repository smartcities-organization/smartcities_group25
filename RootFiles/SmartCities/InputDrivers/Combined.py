# people count publish file
# MQTT Publish Demo
# Publish two messages, to two different topics

import paho.mqtt.publish as publish
import grovepi
import math
import time
import schedule
from grove_rgb_lcd import *
import requests
import urllib.request, json

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
IN_threshold =10
INpeoplecount =0
INcurrentstate = False
INpreviousstate = False
OUT_threshold =20
OUTpeoplecount =0
OUTcurrentstate = False
OUTpreviousstate = False
peoplecount = -1

myhostname = "iot.eclipse.org"

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
	global INpreviousstate
	global INcurrentstate
	global INpeoplecount
	global OUTpreviousstate
	global OUTcurrentstate
	global OUTpeoplecount
	global peoplecount
	
	if distance < IN_threshold :
		INcurrentstate = True
	elif distance < OUT_threshold :
		OUTcurrentstate = True
	else:
		OUTcurrentstate = False
		INcurrentstate = False
	
	if INcurrentstate != INpreviousstate:
		if INcurrentstate == True:
			INpeoplecount=INpeoplecount+1
			publish.single("SmartCities/INpeoplecount", INpeoplecount, hostname=myhostname)
			print("people count updated and published")
		INpreviousstate = INcurrentstate

	if OUTcurrentstate != OUTpreviousstate:
		if OUTcurrentstate == True:
			OUTpeoplecount=OUTpeoplecount+1
			publish.single("SmartCities/OUTpeoplecount", OUTpeoplecount, hostname=myhostname)
			print("people count updated and published")
		OUTpreviousstate = OUTcurrentstate
	
	tpeoplecount = INpeoplecount - OUTpeoplecount
	if tpeoplecount != peoplecount:
		peoplecount = tpeoplecount
		text = "IN =" + str(INpeoplecount) + "  OUT =" + str(OUTpeoplecount) + "\n Inside = " + str(peoplecount)
		#setText("IN = {}  OUT = {}\n Inside = {}".format(str(INpeoplecount)).format(str(OUTpeoplecount)).format(str(peoplecount)))
		setText(text)
		publish.single("SmartCities/peoplecount", peoplecount, hostname=myhostname)
		print(text + "  published")
	

def TempHum_job():
	[temp,humidity] = grovepi.dht(dht_sensor_pin,blue)
	if math.isnan(temp) == False and math.isnan(humidity) == False:
		if temp > 0:
			print("temp = %.02f C humidity =%.02f%%"%(temp, humidity))
			publish.single("SmartCities/Temperature", temp, hostname=myhostname)
			#publish.single("SmartCities/Humidity", humidity, hostname=myhostname)
	else:
		print("nan values")
		#publish.single("SmartCities/Humidity", humidity, hostname=myhostname)
		publish.single("SmartCities/Temperature", temp, hostname=myhostname) 

def LightIntensityCalc_job():
	Intensity = grovepi.analogRead(lightsens_pin)
	#print(Intensity)
	if Intensity < 200:
		LightLevel = "DARK"
	elif Intensity > 200 and Intensity < 400:
		LightLevel = "LOW"
	elif Intensity > 400 and Intensity < 600:
		LightLevel = "MEDIUM"
	elif Intensity > 600 :
		LightLevel = "HIGH"
	publish.single("SmartCities/LightIntensity", LightLevel, hostname=myhostname)

def MotionDetection_job():
	publish.single("SmartCities/MotionDetected", motion, hostname=myhostname)
	#print (1)
def PeopleCount_job():
	#publish.single("SmartCities/peoplecount", peoplecount, hostname=myhostname)
	print(2)

def weather_job():
	api_address = 'https://api.weatherbit.io/v2.0/forecast/hourly?city=Stuttgart,DE&key=fa6a9db81da4407aaf02373b72b2d542&hours=1'
	print("Retrieving Stuttgart temperature for the next hour...")
	response = urllib.request.urlopen(api_address)
	data = json.loads(response.read().decode("utf-8"))
	#print(data)
	weather_temp= data['data'][0]['temp']
	print("Weather forecast : ",weather_temp)
	#print("Current temperature : ", current_temp)
	publish.single("SmartCities/WeatherForecast", weather_temp, hostname=myhostname)


schedule.every(1).minute.at(":10").do(TempHum_job)
#schedule.every(1).minute.at(":10").do(LightIntensityCalc_job)
#schedule.every(1).minute.at(":40").do(LightIntensityCalc_job)
#schedule.every(1).minute.at(":15").do(PeopleCount_job)
#schedule.every(1).minute.at(":20").do(MotionDetection_job)

#schedule.every(5).seconds.do(MotionDetection_job)
#schedule.every(5).seconds.do(PeopleCount_job)
#schedule.every(5).seconds.do(TempHum_job)
schedule.every(5).seconds.do(LightIntensityCalc_job)
schedule.every(6).seconds.do(weather_job)

while True:
	try:
		#PIR Check
		motion=grovepi.digitalRead(pir_sensor_pin)
		#CalcMotionDetection()
		
		# Read distance value from Ultrasonic and calculate people count 
		distance = grovepi.ultrasonicRead(ultrasonic_ranger)
		#print(distance)
		CalcPeopleCount()

		schedule.run_pending()
		time.sleep(.1)
	except TypeError:
        	print ("Error")
	except IOError:
        	print ("Error")
	except (KeyboardInterrupt,SystemExit):
			print("Stopping....")
			#setText("Programm... \n.......Ended")
			sys.exit()
			#setRGB(0,0,0)

sys.exit()

