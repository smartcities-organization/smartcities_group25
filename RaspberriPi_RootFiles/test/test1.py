import time
import paho.mqtt.client as mqtt

def on_message(mqttc,obj,msg):
	print(msg.topic + " " + str(msg.qos) +  " " + str(msg.payload))

def on_subscribe(mqttc,obj,mid,granted_qos):
	print("Subscribed")


mqttc = mqtt.Client()
mqttc.on_subscribe = on_subscribe
mqttc.on_message=on_message

mqttc.connect("test.org",1883,60,)
mqttc.subscribe("38/mclab",0)


