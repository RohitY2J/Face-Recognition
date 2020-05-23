import mysql.connector
from mysql.connector import Error
import cv2

def write_file(data, name):
    # Convert binary data to proper format and write it on Hard Disk
    filename = 'C:\\Users\\dell\\Documents\\python\\Kiran\\photos\\'+str(name)+'.jpg'
    with open(filename, 'wb') as file:
        file.write(data)

def load_image_database():
    names = []
    try:
        #try to develop connection
        connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'rohitkauri123',
            auth_plugin='mysql_native_password',
            database = 'kirancha')

        cursor = connection.cursor()
        cursor.execute("Select * from persons")
        records = cursor.fetchall()
        for record in records:
            names.append(str(record[1]))
            print("Id = ", record[0])
            print("Name = ", record[1])
            image = record[2]
            print("Loading persons image from disk \n")
            write_file(image, record[1])
            
        cursor.close()
        connection.close()
        return names
    except Error as e:
        print("Error while connecting to mysql")
        print(e)
        return null

if __name__ == '__main__':
    load_image_database()
