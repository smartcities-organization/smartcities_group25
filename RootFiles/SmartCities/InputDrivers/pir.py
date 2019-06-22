# for pir motion sensor
import time
import datetime
import grovepi

class Pir:
	def __init__(self, sensor_pin):
		self.sensor_pin = sensor_pin
		self.motion = 0
		grovepi.pinMode(sensor_pin, "INPUT")
	
	def getMotion(self):
		try:
			self.motion=grovepi.digitalRead(self.sensor_pin)
			return self. motion
		except IOError:
			return -1
