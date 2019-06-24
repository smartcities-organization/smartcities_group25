import sqlite3
import time
import datetime
import random
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style
style.use('fivethirtyeight')

import pylab


import numpy as np

plt.plot([1,3,5,9],[1,2,3,4])

plt.show()

conn = sqlite3.connect('tutorial.db')
print('database created')

c= conn.cursor()

def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS stuffToPlot(unix Real, datestmap TEXT,keyword TEXT,value REAL)')

def data_entry():
	c.execute("INSERT INTO stuffToPlot VALUES(1321243,'2016-1-01','Python',5 )")
	conn.commit()
	c.close()
	conn.close()


def dynamic_data_entry():
	unix = int( time.time())
	date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
	keyword ='Python'
	value = random.randrange(0,10)
	c.execute("INSERT INTO stuffToPlot(unix,datestmap,keyword,value)VALUES (?,?,?,?)",
		(unix,date,keyword,value))
	conn.commit()

def read_from_db():
	c.execute("SELECT * FROM stuffToPlot WHERE value = 4 AND keyword='Python'")
	#data = c.fetchall()
	#print(data)
	for row in c.fetchall():
		print(row[0])





##create_table()
#data_entry()
#for i in range(10):
#	dynamic_data_entry()
#	time.sleep(1)

read_from_db()

c.close()
conn.close()