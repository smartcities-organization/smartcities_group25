# for light sensor input drivers
import time
import grovepi

class LightSensor:
	def __init__ (self,sensor_pin,threshold):
		self.sensor_pin = sensor_pin
		self.threshold = threshold
		self.Intensity = 0
		self.IdealLux = 0
		self.resistance =0.0
		grovepi.pinMode(sensor_pin,"INPUT")
	
	def getIntensity(self):
		try:	
			self.Intensity = grovepi.analogRead(self.sensor_pin)
			# convert to lux unit from resistance
			self.resistance = (float)((1023-self.Intensity)*10)/self.Intensity
			return self.resistance
		except IOError:
			print("ERROR.lightsensor")
			return -1

	def getIsEnoughLux(self):
		if self.getIntensity() > self.threshold:
			return True
		elif self.getIntensity() <= self.threshold:
			return False
		else:
			return -1
