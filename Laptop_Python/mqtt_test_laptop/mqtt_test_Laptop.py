import paho.mqtt.publish as publish

publish.single("SmartCities/fromLaptop", "Hello from Laptop", hostname="test.mosquitto.org")
#publish.single("CoreElectronics/topic", "World!", hostname="test.mosquitto.org")
print("Done")