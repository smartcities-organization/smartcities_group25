import tkinter as tk 
r = tk.Tk() 
r.title('Counting Seconds') 


def plot():
    c.execute("SELECT datestmap, value FROM LightData")
    dates=[]
    values=[]
    for row in c.fetchall():
        dates.append(datetime.datetime.fromtimestamp(row[0]))
        values.append(row[1])
    plt.plot_light(dates,values)
    plt.show()

button = tk.Button(r, text='Stop', width=50, command=plot) 
button.pack() 

r.mainloop() 