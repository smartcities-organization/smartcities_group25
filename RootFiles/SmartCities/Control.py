# the main Brain
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
SensorTemp = 24.0
LightIntensity = "LOW"
IsMotionDetected = 0
ForecastTemp1H =24.0
TempUpdated = False
ForecastUpdated = False
TargetTemp = 23


prev_peopleIN =0
prev_peopleOUT =0
prev_peoplecount =0
prev_SensorTemp = 24.0
prev_LightIntensity = "LOW"
prev_IsMotionDetected = 0
prev_ForecastTemp1H = 24.0



#global Flags 
global calcflag 
calcflag = False
global chgCheck 
chgCheck = False
global init_passed 
init_passed = False

openingTime = "08:00"
closingTime = "22:00"
Library_Status = "Close"

## remember it is one hour delayed in R Pi internal clock
time = datetime.now()   
if int(time.hour) >= 8 and int(time.hour) <= 22:
	Library_Status = "Open"
else:
	Library_Status = "Close"

def LineDecode(sline):
	a = sline.split()
	if a[0] == "(switchon":
		if a[1] == "redl)":
			#print ("red led ON")
			publish.single("SmartCities/LedControl", "RedLedON", hostname=myhostname) 
		elif a[1] == "greenl)":
			#print ("green led ON")
			publish.single("SmartCities/LedControl", "GreenLedON", hostname=myhostname) 
		elif a[1] == "bluel)":
			#print("blue led ON")
			publish.single("SmartCities/LedControl", "BlueLedON", hostname=myhostname) 
	elif a[0] == "(switchoff":
		if a[1] == "redl)":
			#print ("red led OFF")
			publish.single("SmartCities/LedControl", "RedLedOFF", hostname=myhostname) 
		elif a[1] == "greenl)":
			#print ("green led OFF")
			publish.single("SmartCities/LedControl", "GreenLedOFF", hostname=myhostname) 
		elif a[1] == "bluel)":
			#print("blue led OFF")
			publish.single("SmartCities/LedControl", "BlueLedOFF", hostname=myhostname) 
	elif a[0] == "(heateron":
		print("heater ON")
	elif a[0] == "(heateroff":
		print ("heater OFF")
	elif a[0] == "(cooleron":
		print("cooler ON")
	elif a[0] == "(cooleroff":
		print ("cooler OFF")



def changeCheck():
	print ("changeCheck called")
	global init_passed
	global calcflag
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
		if ( prev_peopleIN != peopleIN or
			prev_peopleOUT != peopleOUT or
			prev_peoplecount != peoplecount or
			prev_SensorTemp != SensorTemp or
			prev_LightIntensity != LightIntensity or
			prev_IsMotionDetected != IsMotionDetected or
			prev_ForecastTemp1H != ForecastTemp1H ) :
			calcflag = True
			#print("calc 88888888888888888888888888888888888888888888888888888888=" + str(calcflag))
	else:
		prev_peopleIN = peopleIN
		prev_peopleOUT = peopleOUT
		prev_peoplecount = peoplecount
		prev_SensorTemp = SensorTemp
		prev_LightIntensity = LightIntensity
		prev_IsMotionDetected = IsMotionDetected
		prev_ForecastTemp1H = ForecastTemp1H
		print("init_passed = " + str(init_passed))
		init_passed = True

	prev_peopleIN = peopleIN
	prev_peopleOUT = peopleOUT
	prev_peoplecount = peoplecount
	prev_SensorTemp = SensorTemp
	prev_LightIntensity = LightIntensity
	prev_IsMotionDetected = IsMotionDetected
	prev_ForecastTemp1H = ForecastTemp1H

	#print("init_passed = " + str(init_passed))



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
    	peoplecount = int(msg.payload)
    	#print(peoplecount)

    elif msg.topic == "SmartCities/Temperature":
    	global SensorTemp
    	global TempUpdated
    	SensorTemp = round(float(msg.payload))
    	TempUpdated =True
    	#print(SensorTemp)

    elif msg.topic == "SmartCities/LightIntensity":
    	global LightIntensity
    	LightIntensity = msg.payload
    	#print(LightIntensity)

    elif msg.topic == "SmartCities/MotionDetected":
    	global IsMotionDetected
    	IsMotionDetected = int(msg.payload)
    	#print(IsMotionDetected)

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
	#time.sleep(1)
	#print("loop entry")
	if chgCheck is True:
		changeCheck()
		#print("calc 1111111111111111111111111111111111111111111111111111111=" + str(calcflag))
		if calcflag is True:
			print("in Loop")
			#print("calc 555555555555555555555555555555555555555555=" + str(calcflag))

			if peoplecount > 0 and Library_Status == "Open":
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
			#os.system("clear")
			f = open("sas_plan")
			line = f.readline()
			while line.split()[0] != ";":  # this is done to ignore the last line in the plan file
				LineDecode(sline=line)
				line = f.readline()
			f.close()

			##############################################################################
			# Temperature Control Code
			TempUpdated = False
			ForecastUpdated = False
			if ForecastUpdated == True and TempUpdated == True:
				if ForecastTemp1H < SensorTemp:
					Heat = True
				elif ForecastTemp1H > SensorTemp:
					Cool = True
				else:
					Heat = False
					Cool = False

				if SensorTemp > TargetTemp:
					pass
				elif SensorTemp < TargetTemp

			##############################################################################

			#333333333333333333333333333333333333333333333333333333333333
			calcflag = False
		chgCheck = False

	#time.sleep(.5)	
	#print("loop exit")
   


