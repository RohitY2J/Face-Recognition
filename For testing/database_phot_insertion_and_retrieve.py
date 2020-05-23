import mysql.connector 
from mysql.connector import Error
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def write_file(data):
    # Convert binary data to proper format and write it on Hard Disk
    filename = 'C:\\Users\\dell\\Documents\\python\\Kiran\\photos\\a.jpg'
    with open(filename, 'wb') as file:
        file.write(data)

try:
    #try to develop connection
    connection = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'rohitkauri123',
        auth_plugin='mysql_native_password',
        database = 'kirancha')

    cursor = connection.cursor()
    sql_insert_blob_query = """ INSERT INTO persons
                          (id, name, photo) VALUES (%s,%s,%s)"""
    photo = 'C:\\Users\\dell\\Documents\\python\\Kiran\\photos\\kiran.jpg'
    empPicture = convertToBinaryData(photo)
    insert_blob_tuple = (2, "kiran", empPicture)
    result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
    connection.commit()
    '''
    cursor.execute("Select * from persons")
    records = cursor.fetchall()
    for row in records:
        print("Id = ", row[0], )
        print("Name = ", row[1])
        image = row[2]
        print("Storing employee image and bio-data on disk \n")
        write_file(image)
    '''    
    cursor.close()
    connection.close()
except Error as e:
    print("Error while connecting to mysql")
    print(e)

