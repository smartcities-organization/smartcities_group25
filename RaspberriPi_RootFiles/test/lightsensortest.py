#
import grovepi
import time


lightsens_pin = 0


while True:
	try:
		Intensity = grovepi.analogRead(lightsens_pin)
		print(Intensity)
		#resistance = (float)((1023-Intensity)*10)/Intensity
		#print(resistance)
		time.sleep(1)

		if Intensity < 200:
			print("dark")
		elif Intensity > 200 and Intensity < 400:
			print("Low Light")
		elif Intensity > 400 and Intensity < 600:
			print("Med Light")
		elif Intensity > 600 :
			print("High Light")
			pass


		#print("Light Intensity is", resistance)
		#print("Is the light above threshold =",lux)
		#publish.single("SmartCities/LightIntensity", resistance, hostname=myhostname)
		
	except TypeError:
        	print ("Error")
	except IOError:
        	print ("Error")
	except (KeyboardInterrupt,SystemExit):
			print("Stopping....")
			#setText("Programm... \n.......Ended")
			sys.exit()
			#setRGB(0,0,0)

sys.exit()

