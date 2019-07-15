## main function
from pir import Pir
from lightsensor import LightSensor
from grove_dht import Dht 
import time
import datetime
import grovepi
from uv import UVSensor
from threading import Thread

def main():
	pir_sensor_pin = 8
	PIR1 = Pir(pir_sensor_pin)
	lightsens_pin = 0
	lightsensor_thr = 10
	LightSense = LightSensor(lightsens_pin,lightsensor_thr)
	#dht_pin=4
	#dht_pinvalue = dht_pin
	us_pin = 3
	us_sensor =  UVSensor(us_pin)
	us_sensorThread = Thread(target=us_sensor.run)
	us_sensorThread.start()
	
	#print("Before ini")
	#DHT = Dht(dht_pinvalue)
	#print("Before DHT")
	#DHT.start()
	#print("After Dht")
	
	#port = 4
	#sensor = 0
	while True:
		if PIR1.getMotion() == 1:
			print("Motion detected")
		elif PIR1.getMotion()==0:
			print("No motion detected")
		else:
			print("ERROR.PIR")
		time.sleep(5)
		
		resistance = LightSense.getIntensity()
		lux = LightSense.getIsEnoughLux() 
		print("                 Light Intensity is", resistance)
		print("                Is the light above threshold =",lux)
		time.sleep(5)
		
		#string = '[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] '
		try:
			#[Temp , Hum] = grovepi.dht(port,sensor)
			#print(DHT)
			#print(Temp)
			#print(Hum)
			#time.sleep(.8)
	#	temperature,humidity=DHT.feedMe()
		#if not temperature is None :
		#	string += ' [temperature={:.01f}][humidity={:.01f}] '.format(temperature,humidity)
		#else :
		#	string += '[Waiting for Buffer to Fill]'
			
			print('distance=',us_sensor.distance)
			print('count:',us_sensor.peoplecount)
			time.sleep(5)
		except (KeyboardInterrupt,TypeError):
			#DHT.stop()
			us_sensor.terminate()
	#	print(string)


if __name__ == '__main__':
	main()
		
