import time
import sqlite3
from tkinter import *
import matplotlib.pyplot as plt
import matplotlib
import datetime
import grovepi

conn = sqlite3.connect('Database_sensor.db')
Lt= conn.cursor()

buzzer = 8
grovepi.pinMode(buzzer,"OUTPUT")

def plot(*args):
    if selectedPlot.get() == 'Temperature_Plot':
        Lt.execute("SELECT * FROM Data WHERE Topic = 'SmartCities/Temperature'")
        plt.figure()
    elif selectedPlot.get() == 'Humididty_Plot':
        Lt.execute("SELECT * FROM Data WHERE Topic = 'SmartCities/Humidity' ")
        plt.figure()
    elif selectedPlot.get() == 'Motion_Plot':
        Lt.execute("SELECT * FROM Data WHERE Topic = 'SmartCities/Motion' ")
        plt.figure()
    elif selectedPlot.get() == 'PeopleCount_Plot':
        Lt.execute("SELECT * FROM Data WHERE Topic = 'SmartCities/PeopleCount' ")
        plt.figure()
    elif selectedPlot.get() == 'Light_Plot':
        Lt.execute("SELECT * FROM Data WHERE Topic = 'SmartCities/Light' ")
        plt.figure()

    #WHERE topic = temperature
    time_plot= []
    sensor_plot=[]

    for row in Lt.fetchall():
        converted_dates = matplotlib.dates.datestr2num(row[0])
        time_plot.append(converted_dates)
        sensor_plot.append(row[2])              
    plt.xlabel('time')
    plt.ylabel('sensor_data')
    plt.title(selectedPlot.get())
    plt.grid()
    plt.plot_date(time_plot,sensor_plot, '-',label= selectedPlot.get())
    plt.legend(loc ='upper left')
    plt.show()


def BuzzerOff():
    grovepi.digitalWrite(buzzer,0)
    print('Stop Buzzer')

mainwindow = Tk()
mainwindow.configure(background = 'white')
mainwindow.geometry('200x100')
PlotList=["Temperature_Plot", "Humididty_Plot","Motion_Plot","PeopleCount_Plot","Light_Plot"]

selectedPlot = StringVar(mainwindow)
selectedPlot.set(PlotList[0])

PlotMenu= OptionMenu(mainwindow,selectedPlot,*PlotList)
PlotMenu.pack()

button = Button(mainwindow, text="plot", command=plot)
button.pack()

button_buz = Button(mainwindow, text="Turn off Buzzer", command=BuzzerOff)
button_buz.pack()
mainwindow.mainloop()


Lt.close()
conn.close()