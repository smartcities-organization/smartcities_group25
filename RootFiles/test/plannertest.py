#
import os


a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/AllLedOn.pddl --search \"astar(blind())\"")
print (a)
f = open("sas_plan")
print(f.read())
f.close()

a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/AllLedOff.pddl --search \"astar(blind())\"")
print (a)
f = open("sas_plan")
print(f.read())
f.close()

a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/RLedOn.pddl --search \"astar(blind())\"")
print (a)
f = open("sas_plan")
print(f.read())
f.close()

a = os.system("sudo /home/pi/planner/fast-downward.py /home/pi/planner/domain.pddl /home/pi/planner/RGLedOn.pddl --search \"astar(blind())\"")
print (a)
f = open("sas_plan")
print(f.read())
f.close()

