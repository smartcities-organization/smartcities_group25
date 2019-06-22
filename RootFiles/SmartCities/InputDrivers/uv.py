# ultra sound file

from threading import Thread
import time
import grovepi 

class UVSensor:
	def __init__(self, sensor_pin):
		self.sensor_pin= sensor_pin
		self.running = True
		self.peoplecount =0
		self.currentstate = False
		self.previousstate = False
		self.distance=0
		self.threshold =10

	def terminate(self):
       		self.running = False
   
	def run(self):
		while self.running:
			self.distance = grovepi.ultrasonicRead(self.sensor_pin)
			#print('Distance from inside =',self.distance)
			if self.distance < self.threshold:
				self.currentstate = True
			else:
				self.currentstate = False
	#		time.sleep(0.5)
			if self.currentstate != self.previousstate:
				if self.currentstate == True:
					self.peoplecount=self.peoplecount+1
			self.previousstate = self.currentstate
