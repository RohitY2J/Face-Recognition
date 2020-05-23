import tkinter as tk
from tkinter import *
from tkinter import filedialog
import mysql.connector
from mysql.connector import Error
import tkinter.font as font
import csv
from PIL import ImageTk, Image
from functools import partial
import os
from load_database import load_image_database
import shutil

names = []
def show_photo(i):
    small_win = tk.Tk(screenName="Main")          
    
    print(names[i])
    img = ImageTk.PhotoImage(Image.open("C:\\Users\\dell\\Documents\\python\\Kiran\\photos\\"+names[i]+".jpg"),
                             master = small_win)
    panel = tk.Label(small_win, image = img) #set the image
    panel.pack()
    small_win.mainloop()

def select_photo(photo_entry):
    filename = filedialog.askopenfilename(title ='"pen')
    print(filename)
    photo_entry.insert(0, filename)
    return filename

def insert_into_database(win, insert_win, connection, cursor, id_txt, name, filename):
    shutil.copy(filename, 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads')
    statement = "insert into persons values("+id_txt+", '"+name+"', load_file('C:\\\\ProgramData\\\\MySQL\\\\MySQL Server 8.0\\\\Uploads\\\\"+name+".jpg'));"
    print(statement)
    cursor.execute(statement)
    connection.commit()
    print("Inserted into database")
    connection.close()
    database(insert_win)
    
def insert_database(win, connection, cursor):
    win.destroy()
    insert_win = tk.Tk(screenName = "Insert into Database")
    insert_win.geometry("300x250") #You want the size of the app to be 500x500
    insert_win.resizable(0, 0) #Don't allow resizing in the x or y direction
    insert_win.pack_propagate(0)

    title = tk.Label(insert_win, text = "Fill the information", font = "Helvetica 16 bold")
    title.place(relx = 0.5, rely = 0.08, anchor = CENTER)

    id_label = tk.Label(insert_win, text = "Id :")
    id_label.place(relx = 0.2, rely = 0.3, anchor = CENTER)

    id_entry = tk.Entry(insert_win, width = 25)
    id_entry.place(relx = 0.55, rely = 0.3, anchor = CENTER)

    name_label = tk.Label(insert_win, text = "Name :")
    name_label.place(relx = 0.2, rely = 0.5, anchor = CENTER)

    name_entry = tk.Entry(insert_win, width = 25)
    name_entry.place(relx = 0.55, rely = 0.5, anchor = CENTER)

    photo_label = tk.Label(insert_win, text = "Photo :")
    photo_label.place(relx = 0.2, rely = 0.7, anchor = CENTER)

    photo_entry = tk.Entry(insert_win, width = 25)
    photo_entry.place(relx = 0.55, rely = 0.7, anchor = CENTER)    

    select_button = tk.Button(insert_win, text = "Select", command = lambda:select_photo(photo_entry))
    select_button.place(relx = 0.9, rely = 0.7, anchor = CENTER)

    insert_button = tk.Button(insert_win, text = "Insert",
                              command = lambda:insert_into_database(win, insert_win,connection, cursor, id_entry.get(),name_entry.get(),photo_entry.get()),
                              bg = "green", width = 10)
    insert_button.place(relx = 0.5, rely = 0.9, anchor = CENTER)

    insert_win.mainloop()
    

def delete_yes(win, connection, del_win, i, cursor):
    del_win.destroy()
    statement = "Delete from kirancha.persons where Name = '"+names[i]+"'"
    print(statement)
    cursor.execute(statement)
    os.remove("C:\\Users\\dell\\Documents\\python\\Kiran\\photos\\"+names[i]+".jpg")
    connection.commit()
    connection.close()
    
    suc_win = tk.Tk(screenName="Delete")          
    suc_win.geometry("200x100") #You want the size of the app to be 500x500
    suc_win.resizable(0, 0) #Don't allow resizing in the x or y direction
    suc_win.pack_propagate(0)
    print(names[i])
    
    txt = tk.Label(suc_win, text = "Deleted Successfully!!")
    txt.place(relx = 0.5, rely = 0.2, anchor = CENTER)

    no = tk.Button(suc_win, text = "Ok", bg = 'green',
                    command = lambda: delete_no(suc_win), width = 7)
    no.place(relx = 0.5, rely = 0.7, anchor = CENTER)
    suc_win.mainloop()

    

def delete_no(del_win):
    database(del_win)

def delete_data(win,connection, i, cursor):
    win.destroy()
    del_win = tk.Tk(screenName="Delete")          
    del_win.geometry("200x100") #You want the size of the app to be 500x500
    del_win.resizable(0, 0) #Don't allow resizing in the x or y direction
    del_win.pack_propagate(0)
    print(names[i])
    
    txt = tk.Label(del_win, text = "Do you want to delete??")
    txt.place(relx = 0.5, rely = 0.2, anchor = CENTER)
    
    yes = tk.Button(del_win, text = "Yes", bg = 'green',
                    command = lambda: delete_yes(win, connection, del_win, i, cursor), width = 7)
    yes.place(relx = 0.3, rely = 0.7, anchor = CENTER)

    no = tk.Button(del_win, text = "No", bg = 'green',
                    command = lambda: delete_no(del_win), width = 7)
    no.place(relx = 0.7, rely = 0.7, anchor = CENTER)

    del_win.mainloop()

def database(window):
    window.destroy()
    win = tk.Tk()
    load_image_database()
    #heading names for database columns
    col_names = ("Id", "Name", "Photo", "Delete Buttons")
    button_identity = []
    global names
    row = 0  #to keep track of the rows
    
    win.title("Datas from the database")
    #window.destroy()   #destroying previous window
    myFont = font.Font(win, family='Helvetica', size=10, weight='bold')
    
    heading = tk.Label(win, text = "Database data") #heading text
    heading.grid(row = 0,column = 1)
    heading['font'] = myFont

    blank = tk.Label(win, text = "") #leave one row
    blank.grid(row = 1,column = 1)

    
    #try to develop connection
    connection = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'rohitkauri123',
        auth_plugin='mysql_native_password',
        database = 'kirancha')
    db_Info = connection.get_server_info() #get the information about the db
    print("Connected to mysql database with version ",db_Info)
    cursor = connection.cursor() #defining cursor object
    cursor.execute("Select * from persons")
    myresult = cursor.fetchall() #fetch the returned data;

    height = len(myresult)+1  #number of rows + heading
    width = len(myresult[0])+1 #number of columns
    print(width)
    for i in range(height): #Rows
        for j in range(width): #Columns
                if i == 0:
                    # for putting headings
                    b = tk.Label(win, text=col_names[j],
                                     fg = "light green",
                                     bg = "dark green",
                                     width = 20)
                    b.grid(row=i+1, column=j)
                else:
                    #label for id and name
                    if j != 2 and j != 3:
                        b = tk.Label(win, text=myresult[i-1][j], width = 20)
                        b.grid(row=i+1, column=j)
                    elif j == 2:
                        #button for showing photo
                        show = tk.Button(win, text = "Show Photo",bg = 'yellow',
                                         command = partial(show_photo, i-1), width = 19)
                        
                        names.append(myresult[i-1][j-1])
                        show.grid(row = i+1, column = j)
                        print("Show : "+str(j))
                    elif j == 3:
                        #delete button
                        delete = tk.Button(win, text = "Delete Record",bg = 'red',
                                         command = partial(delete_data, win, connection,
                                                           i-1, cursor), width = 19)
                        delete.grid(row = i+1, column = j)
                        print("Delete : "+str(j))
                            
    #button to return
    insert = tk.Button(win,text = "Insert", bg = 'sky blue',
                        command = lambda: insert_database(win, connection, cursor), width = 19)
    insert.grid(row = height+1, column = width-1)

    
    win.mainloop()

if __name__ == '__main__':
    database(tk.Tk())
