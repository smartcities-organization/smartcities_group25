import schedule
import time
import sys
import grovepi
import paho.mqtt.client as mqtt

Motion = 0
buzzer = 8

grovepi.pinMode(buzzer,"OUTPUT")


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


def on_message(client, userdata, msg):
	global Motion

	Motion = msg.payload.decode("utf-8")
	print(Motion)
	
	if Motion == "1":
		print("Buzzer turned on")
		publish.single("SmartCities/Buzzer", "1", hostname="iot.eclipse.org")
		grovepi.digitalWrite(buzzer,1)

	elif Motion == "0":
		print("Room is empty")
		publish.single("SmartCities/Buzzer", "0", hostname="iot.eclipse.org")
		#grovepi.digitalWrite(buzzer,1)

		#time.sleep(600)

        # Stop buzzing for 1 second and repeat
        #grovepi.digitalWrite(buzzer,0)
   

def buzzer_func():
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect("iot.eclipse.org", 1883, 60)
	client.subscribe("SmartCities/Motion")
	client.loop_start()

	

def exit():
	sys.exit()

schedule.every().day.at("23:59").do(buzzer_func)
schedule.every().day.at("06:00").do(exit)

while True:
	try:
		schedule.run_pending()
		time.sleep(10)
	except TypeError:
        	print ("Error")
        	client.disconnect()
        	client.loop_stop()
	except IOError:
        	print ("Error")
        	client.disconnect()
        	client.loop_stop()