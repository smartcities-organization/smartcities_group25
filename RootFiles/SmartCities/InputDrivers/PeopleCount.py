# people count publish file
# MQTT Publish Demo
# Publish two messages, to two different topics

import paho.mqtt.publish as publish
import grovepi

#publish.single("CoreElectronics/test", "Hello", hostname="test.mosquitto.org")
#publish.single("CoreElectronics/topic", "World!", hostname="test.mosquitto.org")


# Connect the Grove Ultrasonic Ranger to digital port D4
# SIG,NC,VCC,GND
ultrasonic_ranger = 3
distance =20
threshold =10
peoplecount =0
currentstate = False
previousstate = False

while True:
	try:
		# Read distance value from Ultrasonic
		distance = grovepi.ultrasonicRead(ultrasonic_ranger)
		if distance < threshold :
			currentstate = True
		else:
			currentstate = False
		#time.sleep(0.5)
		if currentstate != previousstate:
			if currentstate == True:
				peoplecount=peoplecount+1
				publish.single("SmartCities/peoplecount", str(peoplecount), hostname="test.mosquitto.org")
				#print("people count updated and published")
		previousstate = currentstate
	except TypeError:
        	print ("Error")
	except IOError:
        	print ("Error")
