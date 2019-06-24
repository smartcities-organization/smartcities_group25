# MQTT Publish Demo
# Publish two messages, to two different topics

import paho.mqtt.publish as publish

publish.single("SmartCities/test", "Hello", hostname="test.mosquitto.org")
publish.single("SmartCities/topic", "World!", hostname="test.mosquitto.org")
print("Done")