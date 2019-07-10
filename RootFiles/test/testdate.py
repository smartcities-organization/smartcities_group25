#test
from datetime import datetime

a = datetime.now()
print(a.hour)

time = datetime.now() 
if int(time.hour) >= 8 and int(time.hour) <= 22:
	Library_Status = "Open"
	print(Library_Status)
else:
	Library_Status = "Close"
	print(Library_Status)

