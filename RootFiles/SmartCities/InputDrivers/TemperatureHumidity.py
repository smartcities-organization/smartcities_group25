# Publish the Temerature and Humidity 

from grove_dht import Dht
import signal
import sys
import paho.mqtt.publish as publish


dht_sensor = Dht()

def signal_handler(signal, frame):
    global dht_sensor
    dht_sensor.stop()

def callbackFunc():
    global dht_sensor
    print(dht_sensor)
    publish.single("SmartCities/dht", dht_sensor, hostname="test.mosquitto.org")


def Main():
    print("[program is running][please wait]")

    global dht_sensor
    digital_port = 4

    # set the digital port for the DHT sensor
    dht_sensor.setDhtPin(digital_port)
    # using the blue kind of sensor
    # there's also the white one which can be set by calling [dht.setAsWhiteSensor()] function
    dht_sensor.setAsBlueSensor()
    # specifies for how long we record data before we filter it
    # it's better to have larger periods of time,
    # because the statistical algorithm has a vaster pool of values
    dht_sensor.setRefreshPeriod(1)
    # the bigger is the filtering factor (as in the filtering aggresiveness)
    # the less strict is the algorithm when it comes to filtering
    # it's also valid vice-versa
    # the factor must be greater than 0
    # it's recommended to leave its default value unless there is a better reason
    dht_sensor.setFilteringAggresiveness(2.1)
    # every time the Dht object loads new filtered data inside the buffer
    # a callback is what it follows
    dht_sensor.setCallbackFunction(callbackFunc)

    # start the thread for gathering data
    dht_sensor.start()

    # if you want to stop the thread just
    # call dht.stop() and you're done


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    Main()
