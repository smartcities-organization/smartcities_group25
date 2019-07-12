#GUI

import time
import sqlite3
from tkinter import *
import matplotlib.pyplot as plt
import matplotlib
import datetime
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt


Data_tempC = 0
Data_tempD=0
In_people=0
Out_people=0
People_count =0
lux = 0
red_led= 0
green_led =0
blue_led = 0
H_on=0
C_on=0
lib_status=0

conn = sqlite3.connect('Database_SmartLib_Group25.db')
Lt= conn.cursor()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    Data_tempC =msg.payload.decode('utf-8')




def plot(*args):
    if selectedPlot.get() == 'Temperature':
        Lt.execute("SELECT * FROM Data WHERE Topic = 'SmartCities/Temperature'")
        plt.figure()
    elif selectedPlot.get() == 'Heater':
        Lt.execute("SELECT * FROM Data WHERE Topic = 'SmartCities/Humidity' ")
        plt.figure()
    elif selectedPlot.get() == 'Cooler':
        Lt.execute("SELECT * FROM Data WHERE Topic = 'SmartCities/Motion' ")
        plt.figure()
    elif selectedPlot.get() == 'PeopleCount':
        Lt.execute("SELECT * FROM Data WHERE Topic = 'SmartCities/peoplecount' ")
        plt.figure()
    elif selectedPlot.get() == 'LightIntensity':
        Lt.execute("SELECT * FROM Data WHERE Topic = 'SmartCities/LightIntensity' ")
        plt.figure()
    elif selectedPlot.get() == 'RedLed':
        Lt.execute("SELECT * FROM Data WHERE Topic = 'Database/RedLed' ")
        plt.figure()
    elif selectedPlot.get() == 'BlueLed':
        Lt.execute("SELECT * FROM Data WHERE Topic = 'Database/BlueLed' ")
        plt.figure()
    elif selectedPlot.get() == 'GreenLed':
        Lt.execute("SELECT * FROM Data WHERE Topic = 'Database/GreenLed' ")
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
    publish.single("SmartCities/Buzzer", "0", hostname="iot.eclipse.org")
    print("Turn off Buzzer")

def read_database():
    global Data_tempC 
    global Data_tempD
    global In_people
    global Out_people
    global People_count
    global lux
    global red_led
    global green_led
    global blue_led
    global H_on
    global C_on
    global lib_open
    global lib_close

    
    result =0

    Lt.execute("SELECT * FROM Data WHERE Topic ='SmartCities/peoplecount' ORDER BY Datestmp DESC LIMIT 1")
    result = Lt.fetchone()
    People_count = result[2]
    label14.configure(text=People_count)

    result =0

    Lt.execute("SELECT * FROM Data WHERE Topic ='SmartCities/Temperature' ORDER BY Datestmp DESC LIMIT 1")
    result = Lt.fetchone()
    Data_tempC = result[2]
    label3.configure(text= Data_tempC)
    
    result =0

    Lt.execute("SELECT * FROM Data WHERE Topic ='SmartCities/TargetTemperature' ORDER BY Datestmp DESC LIMIT 1")
    result = Lt.fetchone()
    Data_tempD = result[2]
    label4.configure(text= Data_tempD)

    result =0

    Lt.execute("SELECT * FROM Data WHERE Topic ='SmartCities/INpeoplecount' ORDER BY Datestmp DESC LIMIT 1")
    result = Lt.fetchone()
    In_people = result[2]
    label12.configure(text= In_people)

    result =0

    Lt.execute("SELECT * FROM Data WHERE Topic ='SmartCities/OUTpeoplecount' ORDER BY Datestmp DESC LIMIT 1")
    result = Lt.fetchone()
    Out_people = result[2]
    label13.configure(text=Out_people )

    result =0

    Lt.execute("SELECT * FROM Data WHERE Topic ='SmartCities/LightIntensity' ORDER BY Datestmp DESC LIMIT 1")
    result = Lt.fetchone()
    lux= result[2]
    label17.configure(text= lux)

    Lt.execute("SELECT * FROM Data WHERE Topic ='Database/GreenLed' ORDER BY Datestmp DESC LIMIT 1")
    result_g = Lt.fetchone()
    green_led = result_g[2]
    if green_led == '1':
        chkG_state.set(True)
        chkG.configure(var=chkG_state)
    elif green_led == '0':
        chkG_state.set(False)
        chkG.configure(var=chkG_state)

    Lt.execute("SELECT * FROM Data WHERE Topic ='Database/RedLed' ORDER BY Datestmp DESC LIMIT 1")
    result_r = Lt.fetchone()
    red_led= result_r[2]
    if red_led == '1':
        chkR_state.set(True)
        chkR.configure(var=chkR_state)
    elif red_led == '0':
        chkR_state.set(False)
        chkR.configure(var=chkR_state)

    Lt.execute("SELECT * FROM Data WHERE Topic ='Database/BlueLed' ORDER BY Datestmp DESC LIMIT 1")
    result_b = Lt.fetchone()
    blue_led = result_b[2]
    if blue_led == '1':
        chkB_state.set(True)
        chkB.configure(var=chkB_state)
    elif blue_led == '0':
        chkB_state.set(False)
        chkB.configure(var=chkB_state)
        
    result =0

    Lt.execute("SELECT * FROM Data WHERE Topic ='Database/Heater' ORDER BY Datestmp DESC LIMIT 1")
    result = Lt.fetchone()
    H_on = result[2]
    if H_on == '1':
        chkH_state.set(True)
        chkH.configure(var= chkH_state)
    elif H_on =='0':
        chkH_state.set(False)
        chkH.configure(var= chkH_state)

    result =0

    Lt.execute("SELECT * FROM Data WHERE Topic ='Database/Cooler' ORDER BY Datestmp DESC LIMIT 1")
    result = Lt.fetchone()
    C_on = result[2]
    if C_on == '1':
        chkC_state.set(True)
        chkC.configure(var= chkC_state)
    elif C_on =='0':
        chkC_state.set(False)
        chkC.configure(var= chkC_state)

    Lt.execute("SELECT * FROM Data WHERE Topic ='SmartCities/Library_Status' ORDER BY Datestmp DESC LIMIT 1")
    result = Lt.fetchone()
    lib_status = result[2]
    if lib_status == 'Open':
        chkOpen_state.set(True)
        chkClose_state.set(False)
        chkOpen.configure(var= chkOpen_state)
        chkClose.configure(var = chkClose_state)
    elif lib_status =='Close':
        chkOpen_state.set(False)
        chkClose_state.set(True)
        chkOpen.configure(var= chkOpen_state)
        chkClose.configure(var = chkClose_state)


    top.after(2000,read_database)


    



top= Tk()
top.geometry()
top.configure(background='gray10')
top.title('SMART LIBRARY, Group 25')

labelframe1 = LabelFrame(top, text="Temperature",bg='gray10',fg='azure',font =("Calibri(body) bold", 16))  
labelframe1.grid(row=0,column=0,sticky=N+E+W+S)   

labelframe2 = LabelFrame(top, text="Heater & Cooler",bg='gray10',fg='azure',font =("Calibri(body) bold", 16))  
labelframe2.grid(row=0,column=1,sticky=N+E+W+S) 

label1=Label(labelframe1,text="Current Temperature:",bg='gray10',fg='azure',font =("Calibri(body) bold", 16))
label2=Label(labelframe1,text="Default Temperature:",bg='gray10',fg='azure',font =("Calibri(body) bold", 16))
label3=Label(labelframe1,text=Data_tempC,bg='gray10',fg='azure',font =("Calibri(body) bold", 16))
label4=Label(labelframe1,text= Data_tempD,bg='gray10',fg='azure',font =("Calibri(body) bold", 16))

label5=Label(labelframe2,text='Heater On/Off:',bg='gray10',fg='azure',font =("Calibri(body) bold", 16))
label6=Label(labelframe2,text= 'Cooler On/Off:',bg='gray10',fg='azure',font =("Calibri(body) bold", 16))

chkH_state = BooleanVar()
chkH_state.set(False) #set check state
chkH = Checkbutton(labelframe2, text='On', var= chkH_state,font =("Calibri(body)", 16),bg='gray10',fg='azure',selectcolor='black')

chkC_state = BooleanVar()
chkC_state.set(False) #set check state
chkC = Checkbutton(labelframe2, text='On', var= chkC_state,font =("Calibri(body)", 16),bg='gray10',fg='azure',selectcolor='black')

labelframe3 = LabelFrame(top, text="Library",bg='gray10',fg='azure',font =("Calibri(body) bold", 16))  
labelframe3.grid(row=2,column=0,sticky=N+E+W+S) 

chkOpen_state = BooleanVar()
chkOpen_state.set(False) #set check state
chkOpen = Checkbutton(labelframe3, text='Open', var= chkOpen_state,font =("Calibri(body)", 16),bg='gray10',fg='azure',selectcolor='black')

chkClose_state = BooleanVar()
chkClose_state.set(False) #set check state
chkClose = Checkbutton(labelframe3, text='Close', var= chkClose_state,font =("Calibri(body)", 16),bg='gray10',fg='azure',selectcolor='black')

label8=Label(labelframe3,text= 'People Count:',bg='gray10',fg='azure',font =("Calibri(body) bold", 16))
label9=Label(labelframe3,text= "Entering:",bg='gray10',fg='azure',font =("Calibri(body) bold", 16))
label10=Label(labelframe3,text="Exiting :",bg='gray10',fg='azure',font =("Calibri(body) bold", 16))
label11=Label(labelframe3,text="Inside  :",bg='gray10',fg='azure',font =("Calibri(body) bold", 16))

label12=Label(labelframe3,text= In_people,bg='gray10',fg='azure',font =("Calibri(body) bold", 16))
label13=Label(labelframe3,text= Out_people,bg='gray10',fg='azure',font =("Calibri(body) bold", 16))
label14=Label(labelframe3,text= People_count,bg='gray10',fg='azure',font =("Calibri(body) bold", 16))

labelframe4 = LabelFrame(top, text="Light",bg='gray10',fg='azure',font =("Calibri(body) bold", 16))  
labelframe4.grid(row=2,column=1,sticky=N+E+W+S,padx=5) 

chkR_state = BooleanVar()
chkR_state.set(False) #set check state
chkR = Checkbutton(labelframe4, text='Red LED', var= chkR_state,font =("Calibri(body)", 16),bg='gray10',fg='azure',selectcolor='red')

chkG_state = BooleanVar()
chkG_state.set(False)
chkG = Checkbutton(labelframe4, text='Green LED', var= chkG_state,bg='gray10',fg='azure',font =("Calibri(body)", 16),selectcolor='green')

chkB_state = BooleanVar()
chkB_state.set(False) #set check state
chkB = Checkbutton(labelframe4, text='Blue LED', var= chkB_state,bg='gray10',fg='azure',font =("Calibri(body)", 16),selectcolor='blue')

label16=Label(labelframe4,text= 'Intensity:',bg='gray10',fg='azure',font =("Calibri(body) bold", 16))
label17=Label(labelframe4,text=lux,bg='gray10',fg='azure',font =("Calibri(body) bold", 16))
 
labelframe8 = LabelFrame(top,bg='gray10',fg='azure',font =("Calibri(body) bold", 24))  
labelframe8.grid(row=4,column=1,sticky =E,padx=5,pady=5)

btn2= Button(labelframe8, text="EXIT",bg='gray10',fg='azure',font =("Calibri(body) bold", 18), command=top.destroy)

labelframe6 = LabelFrame(top,text='PLOT',bg='gray10',fg='azure',font =("Calibri(body) bold", 16))  
labelframe6.grid(row=3,column=0,padx=5,sticky=N+E+W+S)

PlotList=["Select","Temperature", "Cooler","Heater","PeopleCount","LightIntensity","RedLed","BlueLed","GreenLed"]

selectedPlot = StringVar(top)
selectedPlot.set(PlotList[0])

PlotMenu= OptionMenu(labelframe6,selectedPlot,*PlotList)
PlotMenu.config(pady=5,bg='gray10',fg='azure',font =("Calibri(body)", 16))

button2 = Button(labelframe6, text="Plot", command=plot,bg='gray10',fg='azure',font =("Calibri(body)", 16))

PlotMenu.grid(row=12,column=0)
button2.grid(sticky=E,row=12,column=2,pady=10,padx=5)

labelframe7 = LabelFrame(top,text='ACTUATOR',bg='gray10',fg='azure',font =("Calibri(body) bold", 16))  
labelframe7.grid(row=4,column=0,sticky=N+E+W+S,padx=5)

button3=Button(labelframe7, text="Buzzer Override", command=BuzzerOff,bg='gray10',fg='azure',font =("Calibri(body)", 16))
button3.grid(sticky=W,row=11,column=0)

label1.grid(row=0,column=0)
label3.grid(row=0, column=1)
label2.grid(row=1,column =0)
label4.grid(row=1,column=1)
label5.grid(row=1,column=2,sticky=W)
label6.grid(row=2,column=2)
label8.grid(row=5,column=0,sticky=W)
label9.grid(row=5,column=1,sticky=W)
label10.grid(row=6,column=1,sticky=W)
label11.grid(row=7,column=1,sticky=W)
label12.grid(row=5,column=3)
label13.grid(row=6,column=3)
label14.grid(row=7,column=3)
label16.grid(row=7,column=0,sticky = W)
label17.grid(row=7,column=1)
chkR.grid(row=9,column=0,sticky = W)
chkG.grid(row=8,column=0,sticky = W)
chkB.grid(row=10,column=0,sticky = W)
chkH.grid(row=1,column=3)
chkC.grid(row=2,column=3)
chkOpen.grid(row=3,column=0,sticky=W)
chkClose.grid(row=4,column=0,sticky = W)
btn2.grid()

top.after(0, read_database)
top.mainloop() 

Lt.close()
conn.close()