import requests
import schedule
import time
import urllib.request, json
import paho.mqtt.publish as publish

default_temp = 21
current_temp = 30
myhostname = "iot.eclipse.org"


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


#schedule.every(1).minute.at(":10").do(weather_job)
schedule.every(5).seconds.do(weather_job)

while True :
	schedule.run_pending()
	time.sleep(5)


