import paho.mqtt.publish as publish
import requests
import schedule
import time
import urllib.request, json
import paho.mqtt.client as mqtt
default_temp = 21
current_temp = 30
people_count = 9
led_on = 2
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
def on_message(client, userdata, msg):
	global current_temp

	current_temp = msg.payload.decode("utf-8")
	print(current_temp)

def weather():
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect("iot.eclipse.org", 1883, 60)
	client.subscribe("SmartCities/current_temp")
	#client.loop_start()
	api_address = 'https://api.weatherbit.io/v2.0/forecast/hourly?city=Stuttgart,DE&key=fa6a9db81da4407aaf02373b72b2d542&hours=1'
	print("Retrieving Stuttgart temperature for the next hour...")
	response = urllib.request.urlopen(api_address)
	data = json.loads(response.read())
	weather_temp= data['data'][0]['temp']
	print("Weather forecast : ",weather_temp)
	print("Current temperature : ", current_temp)
	#if ((current_temp in range(28,33))and(round(weather_temp) in range(28,33))):
	#		print("temperature all right!")
	if((round(weather_temp)not in range(21,24))or(round(current_temp)not in range(21,24))):
		if (round(current_temp) in range(21,24)):
			print("temperature all right!")
		elif(round(current_temp)>24):
			print("Switch on the AC!")
			publish.single("Database/Circle1", "circle1_on", hostname="test.mosquitto.org")
			publish.single("Database/Circle1", "circle2_off", hostname="test.mosquitto.org")
		elif(round(current_temp)<21):
			print("Switch on the heater!")
			publish.single("Database/Circle1", "circle2_on", hostname="test.mosquitto.org")
			publish.single("Database/Circle1", "circle1_off", hostname="test.mosquitto.org")
	#else :
	#	if (round(we) in range(20,22)):
	#		print("temperature all right!")
			
	#	elif(round(current_temp)>default_temp):
	#		print("Too hot for the library!")
	#	else :
	#		print("Too cold for the library!")
#schedule.every(0).to(1).minutes.do(w,ather)
	elif((round(weather_temp) in range(21,24))and(round(current_temp)in range(21,24))):
		print("Temperature all right!")

#schedule.every(1).minutes.do(weather)

while True :
		
			weather()
			if(people_count>0 and people_count <= 10):
				if(led_on==1):
					target_temp = target_temp + 0.55
				elif(led_on==2):
					target_temp = target_temp + 1.05
#				print("Temperature has risen by .05 deg C")
				elif(led_on==3):
					target_temp = target_temp + 1.55
			elif(people_count>10 and people_count <= 20):
				if(led_on==1):
					target_temp = target_temp + 0.60
				elif(led_on==2):
					target_temp = target_temp + 1.10
				elif(led_on==3):
					target_temp = current_temp + 1.60
			elif(people_count>30 and people_count <= 40):
				if(led_on==1):
					current_temp = current_temp + 1.05
				elif(led_on==2):
					current_temp = current_temp + 1.55
#				print("Temperature has risen by .05 deg C")
				elif(led_on==3):
					current_temp = current_temp + 2.05
			time.sleep(60)


		#schedule.run_pending()
		
	
