import paho.mqtt.publish as publish
import requests
import schedule
import time
import urllib.request, json
import paho.mqtt.client as mqtt
from datetime import datetime
default_temp = 21
current_temp = 30
people_count = 9
led_on = 2
avg1=0
avg2=0
avg3=0
avg4=0
time_of_day=datetime.now().hour
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
def on_message(client, userdata, msg):
	global current_temp

	current_temp = msg.payload.decode("utf-8")
	print(current_temp)

def weather():
	i=0
	x=6
	y=12
	z=18
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect("iot.eclipse.org", 1883, 60)
	client.subscribe("SmartCities/current_temp")
	#client.loop_start()
	api_address = 'https://api.weatherbit.io/v2.0/forecast/hourly?city=Stuttgart,DE&key=fa6a9db81da4407aaf02373b72b2d542&hours=24'
	#print("Retrieving Stuttgart temperature for the next hour...")
	response = urllib.request.urlopen(api_address)
	data = json.loads(response.read())
	weather_temp= data['data'][0]['temp']
	arr=data['data']
	#print("Weather forecast : ",data)
	hour_day = [arr[0]['temp'],arr[1]['temp'],arr[2]['temp'],arr[3]['temp'],arr[4]['temp'],arr[5]['temp'],
				arr[6]['temp'],arr[7]['temp'],arr[8]['temp'],arr[9]['temp'],arr[10]['temp'],arr[11]['temp'],
				arr[12]['temp'],arr[13]['temp'],arr[14]['temp'],arr[15]['temp'],arr[16]['temp'],arr[17]['temp'],
				arr[18]['temp'],arr[19]['temp'],arr[20]['temp'],arr[21]['temp'],arr[22]['temp'],arr[23]['temp']]
	print ("Temperature array for every hour of the day = ",hour_day)
	if(time_of_day >= 0 and time_of_day <= 5):
		sum1=0
		while i <= 5:
			sum1=sum1+hour_day[i]
			i=i+1
		avg1=sum1/6
		print("Average Temperature for the six hours=", avg1)
	if(time_of_day >= 6 and time_of_day <= 11):
		sum2=0
		while x <= 12:
			sum2=sum2+hour_day[x]
			x=x+1
		avg2=sum2/6
		print("Average Temperature for the six hours=", avg2)
	if(time_of_day >= 12 and time_of_day <= 17):
		sum3=0
		while y <= 18:
			sum3=sum3+hour_day[y]
			y=y+1
		avg3=sum3/6
		print("Average Temperature for the six hours=", avg3)
	if(time_of_day >= 18 and time_of_day <= 23):
		sum4=0
		while z <= 23:
			sum4=sum4+hour_day[z]
			z=z+1
		avg4=sum4/6
		print("Average Temperature for the six hours=", avg4)
			


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
					current_temp = current_temp + 0.55
				elif(led_on==2):
					current_temp = current_temp + 1.05
#				print("Temperature has risen by .05 deg C")
				elif(led_on==3):
					current_temp = current_temp + 1.55
			elif(people_count>10 and people_count <= 20):
				if(led_on==1):
					current_temp = current_temp + 0.60
				elif(led_on==2):
					current_temp = current_temp + 1.10
				elif(led_on==3):
					current_temp = current_temp + 1.60
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
		
	
