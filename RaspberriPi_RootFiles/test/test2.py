import time
import paho.mqtt.client as mqtt

def on_message(mqttc,obj,msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(mqttc,obj,mid):
        print("Published")
        pass


mqttc = mqtt.Client()
mqttc.on_publish = on_publish
mqttc.on_message=on_message

mqttc.connect("test.org",1883,60)
mqttc.publish("38/mclab","data to be sent",0)
