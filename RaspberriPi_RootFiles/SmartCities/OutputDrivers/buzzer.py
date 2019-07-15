#Buzzer

import schedule
import time
import sys
import datetime
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

Motion = 0
client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


def on_message(client, userdata, msg):
	global Motion

	Motion = msg.payload.decode("utf-8")
	print(Motion)
	
	if Motion == "1":
		print("Buzzer turned on")
		publish.single("SmartCities/Buzzer", "1", hostname="iot.eclipse.org")

	elif Motion == "0":
		print("Room is empty")
		publish.single("SmartCities/Buzzer", "0", hostname="iot.eclipse.org")
   

def buzzer_func():
	unix = int( time.time())
	datex = str(datetime.datetime.fromtimestamp(unix).strftime('%I %p'))
	print(datex)
	dt = 'x'
	lt ='y'
	if '00 AM'<datex <'06 AM' :
		client.on_connect = on_connect
		client.on_message = on_message
		client.connect("iot.eclipse.org", 1883, 60)
		client.subscribe("SmartCities/Motion")
		client.loop_start()
		time.sleep(5)

schedule.every(30).seconds.do(buzzer_func)


while True:
	try:
		schedule.run_pending()
		#time.sleep(10)
	except TypeError:
        	print ("Error")
        	client.disconnect()
        	client.loop_stop()
	except IOError:
        	print ("Error")
        	client.disconnect()
        	client.loop_stop()