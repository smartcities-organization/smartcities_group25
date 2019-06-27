import requests
import schedule
import time
import urllib.request, json
default_temp = 21
current_temp = 30

def weather():
	api_address = 'https://api.weatherbit.io/v2.0/forecast/hourly?city=Stuttgart,DE&key=fa6a9db81da4407aaf02373b72b2d542&hours=1'
	print("Retrieving Stuttgart temperature for the next hour...")
	response = urllib.request.urlopen(api_address)
	data = json.loads(response.read())
	weather_temp= data['data'][0]['temp']
	print("Weather forecast : ",weather_temp)
	print("Current temperature : ", current_temp)
	#if ((current_temp in range(28,33))and(round(weather_temp) in range(28,33))):
	#		print("temperature all right!")
	if((round(weather_temp)not in range(28,33))or(round(current_temp)not in range(28,33))):
		if (round(current_temp) in range(30,33)):
			print("temperature all right!")

		elif(round(current_temp)>33):
			print("Switch on the AC!")
		elif(round(current_temp)<28):
			print("Switch on the heater!")
	#else :
	#	if (round(we) in range(20,22)):
	#		print("temperature all right!")
			
	#	elif(round(current_temp)>default_temp):
	#		print("Too hot for the library!")
	#	else :
	#		print("Too cold for the library!")
#schedule.every(0).to(1).minutes.do(w,ather)
	elif((round(weather_temp) in range(28,33))and(round(current_temp)in range(28,33))):
		print("Temperature all right!")
#schedule.every(1).minutes.do(weather)

while True :
		
			weather()
			time.sleep(60)


		#schedule.run_pending()
		
	
