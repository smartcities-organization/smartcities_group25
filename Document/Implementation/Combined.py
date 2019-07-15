# This file take care of all the inputs required for the System
# The raw input value is converted to contextual data and sent to other systems via MQTT 

import paho.mqtt.publish as publish
import grovepi
import math
import time
import schedule
from grove_rgb_lcd import *
import requests
import urllib.request, json
from datetime import datetime
import os

os.system("clear")

setText("Welcome To \nSmart Library")
setRGB(0,128,64)

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

openingTime = "08:00"
closingTime = "22:00"
TimeOpen = 8
TimeClose = 22
Library_Status = "Close"

Ctime = datetime.now()   
if int(Ctime.hour) >= TimeOpen and int(Ctime.hour) < TimeClose:
	Library_Status = "Open"
else:
	Library_Status = "Close"

print(Library_Status)

myhostname = "raspberrypig25"

grovepi.pinMode(lightsens_pin,"INPUT")
grovepi.pinMode(pir_sensor_pin, "INPUT")

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
			if OUTpeoplecount != INpeoplecount:  # to avoid negative values of the people count
				OUTpeoplecount=OUTpeoplecount+1
				publish.single("SmartCities/OUTpeoplecount", OUTpeoplecount, hostname=myhostname)
				print("people count updated and published")
		OUTpreviousstate = OUTcurrentstate
	
	tpeoplecount = INpeoplecount - OUTpeoplecount
	if tpeoplecount != peoplecount:
		peoplecount = tpeoplecount
		text = "IN =" + str(peoplecount) + "  OUT =" + str(OUTpeoplecount) + "\n Total = " + str(INpeoplecount)
		setText(text)
		publish.single("SmartCities/peoplecount", peoplecount, hostname=myhostname)
		print(text + "  published")
	

def Temperature_job():
	[temp,humidity] = grovepi.dht(dht_sensor_pin,blue)
	if math.isnan(temp) == False and math.isnan(humidity) == False:
		if temp > 0:
			print("temp = %.02f C"%(temp))
			publish.single("SmartCities/Temperature", temp, hostname=myhostname)
			#publish.single("SmartCities/Humidity", humidity, hostname=myhostname)
	else:
		print("nan values")
		#publish.single("SmartCities/Humidity", humidity, hostname=myhostname)
		#publish.single("SmartCities/Temperature", temp, hostname=myhostname) 

def Humidity_job():
	[temp,humidity] = grovepi.dht(dht_sensor_pin,blue)
	if math.isnan(temp) == False and math.isnan(humidity) == False:
		if temp > 0:
			print("humidity = %.02f"%(humidity))
			#publish.single("SmartCities/Temperature", temp, hostname=myhostname)
			publish.single("SmartCities/Humidity", humidity, hostname=myhostname)
	else:
		print("nan values")
		#publish.single("SmartCities/Humidity", humidity, hostname=myhostname)
		#publish.single("SmartCities/Temperature", temp, hostname=myhostname) 

def LightIntensityCalc_job():
	global Library_Status
	if Library_Status == "Open":
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
		print("LightIntensity = " + LightLevel)


def PeopleCount_job():
	#publish.single("SmartCities/peoplecount", peoplecount, hostname=myhostname)
	print(2)

def weather_job():
	avg =0
	i=0
	x=6
	y=12
	z=18
	time_of_day = datetime.now().hour # for raspi delay
	api_address = 'https://api.weatherbit.io/v2.0/forecast/hourly?city=Stuttgart,DE&key=fa6a9db81da4407aaf02373b72b2d542&hours=24'
	print("Retrieving Stuttgart temperature for the next 6 hour...")
	response = urllib.request.urlopen(api_address)
	data = json.loads(response.read().decode("utf-8"))
	arr=data['data']
	#print("Weather forecast : ",data)
	hour_day = [arr[0]['temp'],arr[1]['temp'],arr[2]['temp'],arr[3]['temp'],arr[4]['temp'],arr[5]['temp'],
				arr[6]['temp'],arr[7]['temp'],arr[8]['temp'],arr[9]['temp'],arr[10]['temp'],arr[11]['temp'],
				arr[12]['temp'],arr[13]['temp'],arr[14]['temp'],arr[15]['temp'],arr[16]['temp'],arr[17]['temp'],
				arr[18]['temp'],arr[19]['temp'],arr[20]['temp'],arr[21]['temp'],arr[22]['temp'],arr[23]['temp']]
	#print ("Temperature array for every hour of the day = ",hour_day)
	if(time_of_day >= 0 and time_of_day <= 5):
		sum1=0
		while i <= 5:
			sum1=sum1+hour_day[i]
			i=i+1
		avg=sum1/6
		#print("Average Temperature for the six hours=", avg1)
	elif(time_of_day >= 6 and time_of_day <= 11):
		sum2=0
		while x <= 12:
			sum2=sum2+hour_day[x]
			x=x+1
		avg=sum2/6
		#print("Average Temperature for the six hours=", avg2)
	elif(time_of_day >= 12 and time_of_day <= 17):
		sum3=0
		while y <= 18:
			sum3=sum3+hour_day[y]
			y=y+1
		avg=sum3/6
		#print("Average Temperature for the six hours=", avg3)
	elif(time_of_day >= 18 and time_of_day <= 23):
		sum4=0
		while z <= 23:
			sum4=sum4+hour_day[z]
			z=z+1
		avg=sum4/6
		#print("Average Temperature for the six hours=", avg4)
	print("Average Temperature for the six hours=", avg)
	publish.single("SmartCities/WeatherForecast", avg, hostname=myhostname)


def OpenLibrary_job():
	global Library_Status
	Library_Status = "Open"

def CloseLibrary_job():
	global Library_Status
	global INpreviousstate
	global INcurrentstate
	global INpeoplecount
	global OUTpreviousstate
	global OUTcurrentstate
	global OUTpeoplecount
	global peoplecount

	INpreviousstate = False
	INcurrentstate = False
	INpeoplecount = 0
	OUTpreviousstate = False
	OUTcurrentstate = False
	OUTpeoplecount = 0
	peoplecount = 0
	
	publish.single("SmartCities/INpeoplecount", INpeoplecount, hostname=myhostname)
	publish.single("SmartCities/OUTpeoplecount", OUTpeoplecount, hostname=myhostname)
	publish.single("SmartCities/peoplecount", peoplecount, hostname=myhostname)
	Library_Status = "Close"

#schedule.every(1).minute.at(":10").do(LightIntensityCalc_job)
#schedule.every(1).minute.at(":40").do(LightIntensityCalc_job)
#schedule.every(1).minute.at(":15").do(PeopleCount_job)
#schedule.every(1).minute.at(":20").do(MotionDetection_job)
#schedule.every(5).seconds.do(PeopleCount_job)
#schedule.every(5).seconds.do(TempHum_job)
#schedule.every(5).seconds.do(MotionDetection_job)
#schedule.every(20).seconds.do(weather_job)
#schedule.every(10).seconds.do(Temperature_job)
#schedule.every(15).seconds.do(Humidity_job)

schedule.every(3).minute.at(":15").do(TempHum_job)
schedule.every(5).minute.at(":25").do(Humidity_job)
schedule.every(10).seconds.do(LightIntensityCalc_job)

schedule.every().day.at("00:00").do(weather_job)
schedule.every().day.at("06:00").do(weather_job)
schedule.every().day.at("12:00").do(weather_job)
schedule.every().day.at("18:00").do(weather_job)

schedule.every().day.at(openingTime).do(OpenLibrary_job)
schedule.every().day.at(closingTime).do(CloseLibrary_job)


while True:
	try:
		if Library_Status == "Open":
			# Read distance value from Ultrasonic and calculate people count 
			distance = grovepi.ultrasonicRead(ultrasonic_ranger)
			#print(distance)
			CalcPeopleCount()
			motion = 0
			# PIR Sensor is not used during the Library Open hours
			time.sleep(.1)
		else: # Library is closed 
			#PIR Check
			motion=grovepi.digitalRead(pir_sensor_pin)
			publish.single("SmartCities/MotionDetected", motion, hostname=myhostname)
			print("IsMotionDetected = " + str(motion))
			time.sleep(5) # Check PIR every 5 seconds
		schedule.run_pending()
	except TypeError:
        	print ("Error")
	except IOError:
        	print ("Error")
	except (KeyboardInterrupt,SystemExit):
			print("Stopping....")
			sys.exit()
sys.exit()

