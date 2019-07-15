# This file is the Main Control File which receives all the Inputs and 
# derives the output actions from the FD planner. These actions are decoded 
# and sent accordingly to the Actuator file for further Hardware control 

import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time
import schedule
import os
from datetime import datetime

os.system("clear")

myhostname = "raspberrypig25"

peopleIN =0
peopleOUT =0
peoplecount =0
SensorTemp = 23.0
LightIntensity = "LOW"
IsMotionDetected = 0
ForecastTemp1H =23.0
TargetTemp = 23
heater_on = False
cooler_on = False
SensorHum = 40
Humidifier_Status = "None"

TempUpdated = True
HumUpdated = True
ForecastUpdated = True
LightIntensityUpdate = True
peoplecountUpdated = True

prev_peopleIN =0
prev_peopleOUT =0
prev_peoplecount =0
prev_SensorTemp = 24.0
prev_LightIntensity = "LOW"
prev_IsMotionDetected = 0
prev_ForecastTemp1H = 24.0
prev_TargetTemp = 23
prev_SensorHum = 0

red = False
green = False
blue =False


#global Flags 
global calcflag 
calcflag = True
global chgCheck 
chgCheck = True
global init_passed 
init_passed = False

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

publish.single("SmartCities/Library_Status", Library_Status, hostname=myhostname)

def LineDecode(sline):
	global heater_on
	global cooler_on
	global red 
	global green 
	global blue
	global Humidifier_Status

	a = sline.split()
	if a[0] == "(switchon":
		if a[1] == "redl)":
			print ("red led ON")
			red = True
			publish.single("Actuator/LedControl", "RedLedON", hostname=myhostname) 
		elif a[1] == "greenl)":
			print ("green led ON")
			green = True
			publish.single("Actuator/LedControl", "GreenLedON", hostname=myhostname) 
		elif a[1] == "bluel)":
			print("blue led ON")
			blue = True
			publish.single("Actuator/LedControl", "BlueLedON", hostname=myhostname) 
	elif a[0] == "(switchoff":
		if a[1] == "redl)":
			print ("red led OFF")
			red = False
			publish.single("Actuator/LedControl", "RedLedOFF", hostname=myhostname) 
		elif a[1] == "greenl)":
			print ("green led OFF")
			green = False
			publish.single("Actuator/LedControl", "GreenLedOFF", hostname=myhostname) 
		elif a[1] == "bluel)":
			print("blue led OFF")
			blue = False
			publish.single("Actuator/LedControl", "BlueLedOFF", hostname=myhostname) 
	elif a[0] == "(heateron":
		print("heater ON")
		heater_on =True
		if cooler_on == True:
			print ("cooler OFF")
			publish.single("Actuator/Cooler", "cool_off", hostname=myhostname)
			cooler_on = False
		publish.single("Actuator/Heater", "heat_on", hostname=myhostname)
	elif a[0] == "(heateroff":
		print ("heater OFF")
		heater_on = False
		publish.single("Actuator/Heater", "heat_off", hostname=myhostname)
	elif a[0] == "(cooleron":
		print("cooler ON")
		cooler_on = True
		if heater_on == True :
			print ("heater OFF")
			publish.single("Actuator/Heater", "heat_off", hostname=myhostname)
			heater_on = False
		publish.single("Actuator/Cooler", "cool_on", hostname=myhostname)
	elif a[0] == "(cooleroff":
		print ("cooler OFF")
		cooler_on = False
		publish.single("Actuator/Cooler", "cool_off", hostname=myhostname)
	elif a[0] == "(on_dehumidifier":
		print("De-Humidifier ON")
		Humidifier_Status = "De-Humidifier ON"
		publish.single("Database/Humidity_Control", "dehumidifier_on", hostname=myhostname)
	elif a[0] == "(on_humidifier":
		print("Humidifier ON")
		Humidifier_Status = "Humidifier ON"
		publish.single("Database/Humidity_Control", "humidifier_on", hostname=myhostname)
	elif a[0] == "(off_hum_dehum":
		print("Both Humidifier and De-Humidifier OFF")
		Humidifier_Status = "Both Humidifier and De-Humidifier OFF"
		publish.single("Database/Humidity_Control", "both_off", hostname=myhostname)


def changeCheck():
	print ("changeCheck called")
	global init_passed
	global calcflag
	global peopleIN 
	global peopleOUT 
	global peoplecount 
	global SensorTemp 
	global SensorHum
	global LightIntensity 
	global IsMotionDetected 
	global ForecastTemp1H 

	global prev_peopleIN 
	global prev_peopleOUT 
	global prev_peoplecount 
	global prev_SensorTemp 
	global prev_SensorHum 
	global prev_LightIntensity
	global prev_IsMotionDetected
	global prev_ForecastTemp1H


	if init_passed is True :
		if ( prev_peopleIN != peopleIN or
			prev_peopleOUT != peopleOUT or
			prev_peoplecount != peoplecount or
			prev_SensorTemp != SensorTemp or
			prev_SensorHum != SensorHum or
			prev_LightIntensity != LightIntensity or
			prev_IsMotionDetected != IsMotionDetected or
			prev_ForecastTemp1H != ForecastTemp1H ) :
			calcflag = True
	else:
		prev_peopleIN = peopleIN
		prev_peopleOUT = peopleOUT
		prev_peoplecount = peoplecount
		prev_SensorTemp = SensorTemp
		prev_SensorHum = SensorHum
		prev_LightIntensity = LightIntensity
		prev_IsMotionDetected = IsMotionDetected
		prev_ForecastTemp1H = ForecastTemp1H
		print("init_passed = " + str(init_passed))
		init_passed = True

	prev_peopleIN = peopleIN
	prev_peopleOUT = peopleOUT
	prev_peoplecount = peoplecount
	prev_SensorTemp = SensorTemp
	prev_SensorHum = SensorHum
	prev_LightIntensity = LightIntensity
	prev_IsMotionDetected = IsMotionDetected
	prev_ForecastTemp1H = ForecastTemp1H


def TargetTemperatureCalc():

	global TargetTemp
	global peoplecount
	global red 
	global green 
	global blue
	global prev_TargetTemp
	global TempUpdated

	if red is True and green is True and blue is True:
		LedCount = 3
	elif red is True and green is True and blue is False:
		LedCount = 2
	elif red is True and green is False and blue is False:
		LedCount = 1
	elif red is False and green is False and blue is False:
		LedCount = 0

	# the assumption is that each person on average generates heat approx 0.1 deg and each light by 0.5 deg
	# 0.1/0.5 deg is hard coded just to show the increse in the temp
	# but not in reality it needs to be calibrated

	TargetTemp = 23 - (peoplecount * 0.1) - (LedCount * 0.5)
	print( "updated Target = " + str(TargetTemp))
	publish.single("SmartCities/TargetTemperature", TargetTemp, hostname=myhostname)

	if prev_TargetTemp != TargetTemp:
		print(prev_TargetTemp)
		print(TargetTemp)
		TempUpdated = True  # TempUpdated flag is used for both Sensor Temperature and Target Temperature changes 
		prev_TargetTemp = TargetTemp

#MQTT Callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    msg.payload = msg.payload.decode("utf-8")
    global chgCheck

    if msg.topic == "SmartCities/INpeoplecount":
    	global peopleIN
    	peopleIN = int(msg.payload)
    	#print(peopleIN)

    elif msg.topic == "SmartCities/OUTpeoplecount":
    	global peopleOUT
    	peopleOUT = int(msg.payload)
    	#print(peopleOUT)

    elif msg.topic == "SmartCities/peoplecount":
    	global peoplecount
    	global peoplecountUpdated
    	peoplecountUpdated = True
    	peoplecount = int(msg.payload)
    	#print(peoplecount)

    elif msg.topic == "SmartCities/Temperature":
    	global SensorTemp
    	global TempUpdated
    	SensorTemp = round(float(msg.payload))
    	TempUpdated =True
    	#print(SensorTemp)

    elif msg.topic == "SmartCities/Humidity":
    	global SensorHum
    	global HumUpdated
    	SensorHum = round(float(msg.payload))
    	print(SensorHum)
    	HumUpdated =True

    elif msg.topic == "SmartCities/LightIntensity":
    	global LightIntensity
    	global LightIntensityUpdate
    	LightIntensityUpdate = True
    	LightIntensity = msg.payload
    	#print(LightIntensity)

    elif msg.topic == "SmartCities/MotionDetected":
    	global IsMotionDetected
    	IsMotionDetected = int(msg.payload)
    	print(IsMotionDetected)

    elif msg.topic == "SmartCities/WeatherForecast":
    	global ForecastTemp1H
    	global ForecastUpdated
    	ForecastTemp1H = round(float(msg.payload))
    	ForecastUpdated =True
    	#print(ForecastTemp1H)
    chgCheck = True

def OpenLibrary_job():
	global Library_Status
	Library_Status = "Open"
	publish.single("SmartCities/Library_Status", Library_Status, hostname=myhostname)

def CloseLibrary_job():
	global Library_Status
	Library_Status = "Close"
	publish.single("SmartCities/Library_Status", Library_Status, hostname=myhostname) 


schedule.every().day.at(openingTime).do(OpenLibrary_job)
schedule.every().day.at(closingTime).do(CloseLibrary_job)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(myhostname,1883,60)
client.subscribe("SmartCities/#")
client.loop_start()

while True:
	time.sleep(0.5)  # time for MQTT to perform its checks
	client.loop_stop()
	if chgCheck is True:
		changeCheck()
		if calcflag is True:
			
			print("in Loop")

			##############################################################################
			# Lighting Control Code
			if (peoplecountUpdated == True or LightIntensityUpdate == True) and Library_Status == "Open":
				if peoplecount > 0:
					if LightIntensity == "DARK":
						a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/AllLedOn.pddl --search \"astar(blind())\"")
					elif LightIntensity == "LOW":
						a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/RLedOn.pddl --search \"astar(blind())\"")
					elif LightIntensity == "MEDIUM":
						a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/RGLedOn.pddl --search \"astar(blind())\"")
					elif LightIntensity == "HIGH":
						a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/AllLedOff.pddl --search \"astar(blind())\"")
				else:
					a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/AllLedOff.pddl --search \"astar(blind())\"")
				
				f = open("sas_plan")
				line = f.readline()
				while line.split()[0] != ";":  # this is done to ignore the last line in the plan file
					LineDecode(sline=line)
					line = f.readline()
				f.close()

				peoplecountUpdated = False
				LightIntensityUpdate = False

			TargetTemperatureCalc()

			##############################################################################
			# Temperature Control Code
			if ForecastUpdated == True or TempUpdated == True:
				if ForecastTemp1H < TargetTemp:
					Heat = True
					Cool = False
				elif ForecastTemp1H > TargetTemp:
					Cool = True
					Heat = False
				else:
					Heat = False
					Cool = False


				if SensorTemp > TargetTemp and Heat == True and Cool == False:  
					a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/HeaterOff.pddl --search \"astar(blind())\"")
					# Surrounding is Cold and Sensor is also hot so turn off Heat

				elif SensorTemp > TargetTemp and Heat == False:# (Cool == True or Cool == False): 
					a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/CoolerOn.pddl --search \"astar(blind())\"")
					# Surrounding is Hot and Sensor is also hot so turn on cool
				
				elif SensorTemp < TargetTemp and  Cool == False: #(Heat == True or False)
					a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/HeaterOn.pddl --search \"astar(blind())\"") 
					# Surrounding is Cold and Sensor is also Cold so turn on Heat
				
				elif SensorTemp < TargetTemp and Heat == False and Cool == True:  
					a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/CoolerOff.pddl --search \"astar(blind())\"")
					# Surrounding is Hot and Sensor is also cold so turn off cool

				elif SensorTemp == TargetTemp:  
					# Surrounding is equal to target and sensor also equal to target
					if heater_on == True:
						a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/HeaterOff.pddl --search \"astar(blind())\"")
						# turn off Heater
					elif cooler_on == True:
						a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/CoolerOff.pddl --search \"astar(blind())\"")
						# Turn off Cooler
				
				f = open("sas_plan")
				line = f.readline()
				while line.split()[0] != ";":  # this is done to ignore the last line in the plan file
					LineDecode(sline=line)
					line = f.readline()
				f.close()
				
				TempUpdated =False
				ForecastUpdated = False

			##############################################################################
			# Humidity Control Code

			if(HumUpdated == True):
				if(SensorHum<30):
					a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/hum_ON.pddl --search \"astar(blind())\"")
				elif(SensorHum>50):
					a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/dehum_ON.pddl --search \"astar(blind())\"")
				elif(SensorHum>=30 and SensorHum<=50):
					a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/AllHum_off.pddl --search \"astar(blind())\"")
				
				f = open("sas_plan")
				line = f.readline()
				while line.split()[0] != ";":  # this is done to ignore the last line in the plan file
					LineDecode(sline=line)
					line = f.readline()
				f.close()
				
				HumUpdated =False

			calcflag = False


			##############################################################################
			# Alarm Control Code
			if Library_Status == "Close":
				if IsMotionDetected == 1:
					publish.single("Actuator/Buzzer", "BuzzerOn", hostname=myhostname)
					

		chgCheck = False

		print("Library_Status = " + Library_Status +"\nWeatherForecast = "+str(ForecastTemp1H)+ "\nTarget = " + str(TargetTemp) + "\nSensorTemp = " + str(SensorTemp) + "\npeoplecount = " + str(peoplecount) + "\nLightIntensity = " + LightIntensity )
		print("IsMotionDetected = " + str(IsMotionDetected) + "\nHumidity =" + str(SensorHum))
		print("Humidifier_Status = " + Humidifier_Status)
	client.loop_start()