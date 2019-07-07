# testing schedule library
import schedule
import time
import paho.mqtt.publish as publish

def job():
    print("I'm working...")
    print(time.ctime())
    #publish.single("SmartCities/test", "schedule test", hostname="test.mosquitto.org")


#schedule.every(10).minutes.do(job)
#schedule.every().hour.do(job)
#schedule.every().day.at("10:30").do(job)
#schedule.every().monday.do(job)
#schedule.every().wednesday.at("13:15").do(job)
#schedule.every(1).minute.at(":05").do(job)
#schedule.every().minute.at(":25").do(job)
#schedule.every().minute.at(":35").do(job)
#schedule.every().minute.at(":45").do(job)
#schedule.every().minute.at(":55").do(job)
#schedule.every().second.do(job)
schedule.every(5).second.do(job)

while True:
    schedule.run_pending()
    time.sleep(0.5)
