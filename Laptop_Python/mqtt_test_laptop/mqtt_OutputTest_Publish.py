# MQTT Publish Demo
# Publish two messages, to two different topics

import paho.mqtt.publish as publish
import sys


publish.single("SmartCities/test",sys.argv[1], hostname="test.mosquitto.org")
#publish.single("SmartCities/topic", "World!", hostname="test.mosquitto.org")

#print(sys.argv)
#print(sys.argv[0])
#print(sys.argv[1])


print("Done")