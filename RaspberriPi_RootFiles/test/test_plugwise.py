#
from plugwise.api import*
import time
from datetime import datetime

DEFAULT_PORT ="/dev/ttyUSB0"
mac1="000D6F000278F2F3"
mac2="000D6F0002C0EB54"
stick = Stick(DEFAULT_PORT)
circle1 = Circle (mac1, stick)
circle2 = Circle (mac2, stick)
dt = datetime.now()

#circle1.set_clock (dt)
#circle2.set_clock (dt)


circle1.switch_off ()
circle2.switch_off ()
time.sleep(2)

print (circle1.get_info())
print (circle2.get_info())

print (circle1.get_clock())
print (circle2.get_clock())


circle1.switch_on ()
circle2.switch_on ()
time.sleep(2)
print (circle1.get_info())
print (circle2.get_info())

print (circle1.get_clock())
print (circle2.get_clock())
time.sleep(2)

print ("Current electricity consumption in W: %.2f" %(circle1.get_power_usage()))
print ("Current electricity consumption in W: %.2f" %(circle2.get_power_usage()))
time.sleep(2)

circle1.switch_off ()
time.sleep(2)

circle2.switch_off ()
time.sleep(2)

print ("Current electricity consumption in W: %.2f" %(circle1.get_power_usage()))
print ("Current electricity consumption in W: %.2f" %(circle2.get_power_usage()))

print (circle1.get_power_usage_history(None))
print (circle2.get_power_usage_history(None))

