import time
import grovepi
from grovepi import *

# Connect the Grove LED to digital port D4
led = 4
pir_motion = 8

pinMode(led,"OUTPUT")
pinMode(pir_motion,"INPUT")
time.sleep(1)

print ("This example will blink a Grove LED connected to the GrovePi+ on the port labeled D4.\nIf you're having trouble seeing the LED blink, be sure to check the LED connection and the po$")
print (" ")
print ("Connect the LED to the port labele D4!" )

while True:
	try:
		motion=grovepi.digitalRead(pir_motion)
		if motion==1:
			#Blink the LED
			digitalWrite(led,1)             # Send HIGH to switch on LED
			print("motion Detected")
			time.sleep(1)
			digitalWrite(led,0)             # Send LOW to switch off LED
			print("motion Detected")
			time.sleep(1)
		elif motion==0:
			digitalWrite(led,0)             # Send LOW to switch off LED
			print("No Motion")
			time.sleep(1)
		else:
			print("Error")
	except KeyboardInterrupt:   # Turn LED off before stopping
		digitalWrite(led,0)
		break
	except IOError:                             # Print "Error" if communication error encountered
		print("Error")
