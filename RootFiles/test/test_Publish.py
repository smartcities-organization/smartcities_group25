# MQTT Publish Demo
# Publish two messages, to two different topics

import paho.mqtt.publish as publish
import sys

myhostname = "raspberrypig25"
publish.single("SmartCities/Humidity",sys.argv[1], hostname=myhostname)
#publish.single("SmartCities/topic", "World!", hostname="test.mosquitto.org")

#print(sys.argv)
#print(sys.argv[0])
#print(sys.argv[1])


print("Done")
