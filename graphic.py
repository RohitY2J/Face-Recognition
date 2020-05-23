import tkinter as tk           #importing tkinter
import tkinter.font as font
from PIL import ImageTk, Image
import os
from datas import database
from tkinter import Menu

import serial
import time
import csv
import matplotlib
matplotlib.use("tkAgg")
import matplotlib.pyplot as plt
import numpy as np

'''y_var = np.array(np.zeros([20]))
fig = ""
ax = ""
line =""
times = 1
arr = []
ser = ""

def serial_read(root,port_num, baud_rate):
    global ser
    ser = serial.Serial()
    ser.baudrate = baud_rate
    ser.port = port_num
    ser.port : port_num
    ser.open()
    root.after(2, serial_read2(root))

def serial_read2(root):
    global y_var, arr, fig, ax, line, times, ser
    try:
        ser_bytes = ser.readline()
        decoded_bytes = ser_bytes.decode('utf-8')
        print("\n"+str(decoded_bytes))
        arr.append(decoded_bytes)
        print(len(arr))  
        print("============="+str(times))
        if len(arr) == 5:
            print(type(arr[2]))
            print("Data needed:"+str(arr[2]))
            y_var = np.append(y_var,int(arr[2]))
            y_var = y_var[1:20+1]
            line.set_ydata(y_var)
            ax.relim()
            ax.autoscale_view()
            fig.canvas.draw()
            fig.canvas.flush_events()
            arr = []
            times = times + 1
        root.after(1, serial_read2(root))
    except:
    	print("Keyboard Interrupt")
    	y_var = np.array(np.zeros([20]))
    	fig = ""
    	ax = ""
    	line =""
    	times = 1
    	arr = []
    	ser = ""

#start reading the data from serial port
def read(window,port_num, baud_rate):
    global fig, ax, line
    y_var = np.array(np.zeros([20]))
    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot(y_var)
    serial_read(window,port_num, baud_rate) #read the data



def main_read(win):
    win.destroy()
    #window description    
    window = tk.Tk(screenName="Main",  baseName="What is this??",  useTk=1)          
    window.title('Hello, Tkinter!')
    window.geometry('500x300') # Size 200, 200
    window.resizable(False, False) #dont resize the window

    #creating menubar
    menubar = Menu(window)
    filemenu = Menu(menubar, tearoff=0)
    #add submenu
    filemenu.add_command(label="New", command=donothing)
    filemenu.add_command(label="Open", command=donothing)
    filemenu.add_command(label="Save", command=donothing)
    menubar.add_cascade(label="File", menu=filemenu) #add the menu
    #action submenu
    action_menu = Menu(menubar, tearoff=0)
    action_menu.add_command(label="Read", command= lambda: main_read(window))
    action_menu.add_command(label="Show database", command= lambda: main_database(window))
    menubar.add_cascade(label="Action", menu=action_menu) 

    img = ImageTk.PhotoImage(Image.open("dave.jpg")) #icon image
    panel = tk.Label(window, image = img) #set the image
    panel.place(relx = 0.44, rely = 0.1)

    #label and entry defining
    port_num = tk.Label(window, text="Port Number")
    port_num.place(relx = 0.05, rely = 0.42)
    port_num_entry = tk.Entry(window, width = 29)
    port_num_entry.place(relx=0.3, rely=0.42)

    baud_rate_label = tk.Label(window, text="Baudrate")
    baud_rate_label.place(relx = 0.05, rely = 0.52)
    baud_rate_entry = tk.Entry(window, width = 29)
    baud_rate_entry.place(relx=0.3, rely=0.52)

    #button defining
    button_read = tk.Button(window, text = "Read", width = 25, bg = 'green', command = lambda: read(window,port_num_entry.get(),baud_rate_entry.get()))
    button_read.place(relx = 0.25, rely = 0.65)
    button_exit = tk.Button(window, text='exit', width=25, bg = 'green',command=window.destroy)
    button_exit.place(relx=0.25, rely=0.78)

    #defining the font of the button and label
    myFont = font.Font(family='Helvetica', size=10, weight='bold')

    button_exit['font'] = myFont
    button_read['font'] = myFont
    port_num_entry['font'] = myFont
    baud_rate_entry['font'] = myFont

    window.config(menu = menubar)
    window.mainloop()

'''	

def open_data(window, user, pwd):
    if user == "Kiran1920" and pwd == "@#$12390":
        database(window)

def donothing():
    return



def main_database(win):
    win.destroy()
    #window description    
    window = tk.Tk(screenName="Main",  baseName="What is this??",  useTk=1)          
    window.title('Hello, Tkinter!')
    window.geometry('500x400') # Size 200, 200
    window.resizable(False, False) #dont resize the window

    img = ImageTk.PhotoImage(Image.open("./photos/bp.jpg")) #icon image
    panel = tk.Label(window, image = img) #set the image
    panel.place(relx = 0.24, rely = 0.05)

    user_label = tk.Label(window, text = "User Name:")
    user_label.place(relx = 0.05, rely = 0.55)
    user_entry = tk.Entry(window, width = 29)
    user_entry.place(relx = 0.3, rely = 0.55)
    
    pwd_label = tk.Label(window, text = "Enter password:")
    pwd_label.place(relx = 0.05, rely = 0.61)
    pwd_entry = tk.Entry(window, width = 29, show = "*")
    pwd_entry.place(relx = 0.3, rely = 0.61)

    #button defining
    button_login = tk.Button(window, text='Login', width=25, bg = 'green',
                             command = lambda: open_data(window, user_entry.get(),
                                                         pwd_entry.get()))
    button_login.place(relx=0.25, rely=0.69)
    button_exit = tk.Button(window, text='Exit', width=25, bg = 'green',
                            command=window.destroy)
    button_exit.place(relx=0.25, rely=0.78)

    #defining the font of the button and label
    myFont = font.Font(family='Helvetica', size=10, weight='bold')

    button_exit['font'] = myFont
    
    button_login['font'] = myFont
    user_entry['font'] = myFont
    pwd_entry['font'] = myFont

    window.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    main_database(root)
