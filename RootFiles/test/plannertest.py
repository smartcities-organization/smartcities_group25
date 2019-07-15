#
import os

def LineDecode(sline):
	a = sline.split()
	if a[0] == "(switchon":
		if a[1] == "redl)":
			print ("red led ON")
		elif a[1] == "greenl)":
			print ("green led ON")
		elif a[1] == "bluel)":
			print("blue led ON")
	elif a[0] == "(switchoff":
		if a[1] == "redl)":
			print ("red led OFF")
		elif a[1] == "greenl)":
			print ("green led OFF")
		elif a[1] == "bluel)":
			print("blue led OFF")
	elif a[0] == "(heateron":
		print("heater ON")
	elif a[0] == "(heateroff":
		print ("heater OFF")
	elif a[0] == "(cooleron":
		print("cooler ON")
	elif a[0] == "(cooleroff":
		print ("cooler OFF")
	elif a[0] == "(on_dehumidifier":
		print("De-Humidifier ON")
	elif a[0] == "(on_humidifier":
		print("Humidifier ON")
	elif a[0] == "(off_hum_dehum":
		print("Both Humidifier and De-Humidifier OFF")



# a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/AllLedOn.pddl --search \"astar(blind())\"")
# a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/AllLedOff.pddl --search \"astar(blind())\"")
# a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/RLedOn.pddl --search \"astar(blind())\"")
# a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/RGLedOn.pddl --search \"astar(blind())\"")
# a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/HeaterOn.pddl --search \"astar(blind())\"")
# a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/HeaterOff.pddl --search \"astar(blind())\"")
# a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/CoolerOn.pddl --search \"astar(blind())\"")
#a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/CoolerOff.pddl --search \"astar(blind())\"")
#a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/AllHum_off.pddl --search \"astar(blind())\"")
a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/dehum_ON.pddl --search \"astar(blind())\"")
#a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/hum_ON.pddl --search \"astar(blind())\"")

#os.system("clear")
print (a)
f = open("sas_plan")
# l1 = f.readline()
# if l1 is not None:
# 	(first,rest)=l1.split(maxsplit=2)
# 	print(first)
# 	print(rest)
# 	print(rr)
line = f.readline()
while line.split()[0] != ";":
	#print(line.split()[0])
	#print(line.split()[1])
	#print(line)
	LineDecode(sline=line)
	line = f.readline()
f.close()


#f = open("sas_plan")
#line = f.readline()
#while line.split()[0] != ";":
#	LineDecode(sline=line)
#	line = f.readline()
#f.close()
