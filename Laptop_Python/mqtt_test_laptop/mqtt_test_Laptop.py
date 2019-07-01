import paho.mqtt.publish as publish

publish.single("SmartCities/Temperature", 300, hostname="iot.eclipse.org")
#publish.single("CoreElectronics/topic", "World!", hostname="test.mosquitto.org")
print("Done")