# MQTT Publish Demo
# Publish two messages, to two different topics

import paho.mqtt.publish as publish
import sys

myhostname = "raspberrypig25"

if sys.argv[1] == "T":
	publish.single("SmartCities/Temperature",sys.argv[2], hostname=myhostname)
elif sys.argv[1] == "W":
	publish.single("SmartCities/WeatherForecast", sys.argv[2], hostname=myhostname)
elif sys.argv[1] == "H":
	publish.single("SmartCities/Humidity", sys.argv[2], hostname=myhostname)

print(sys.argv)
#print(sys.argv[0])
#print(sys.argv[1])


print("Done")
