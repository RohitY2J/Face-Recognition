
######  importing necessary modules

import matplotlib.pyplot as pyplot
from mtcnn import MTCNN
from PIL import Image
import numpy as np
from keras_vggface.utils import preprocess_input
from scipy.spatial.distance import cosine
import tensorflow as tf
from keras.models import load_model
from keras.models import model_from_json

import cv2
from mtcnn import MTCNN

from keras_vggface.vggface import VGGFace
from keras.applications import ResNet50

import smtplib

import mysql.connector
from mysql.connector import Error
import cv2

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os

var = 35
##### take picture 
cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop) 

while(True):
    ret,frame = cap.read() # return a single frame in variable `frame`
    cv2.imshow('frame',frame) #display the captured image
    if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y' 
        cv2.imwrite('C:\\Users\\dell\\Documents\\python\\Kiran\\photos\\This Pic.jpg',frame)
        cv2.destroyAllWindows()
        break

cap.release()
cv2.destroyAllWindows()
print('Progress................... 10%')

###### extract a single face from a given photograph
def extract_face(filename, required_size=(224, 224)):
	# load image from file
	pixels = pyplot.imread(filename)
	global var
	# create the detector, using default weights
	detector = MTCNN()
	# detect faces in the image
	results = detector.detect_faces(pixels)
	# extract the bounding box from the first face
	x1, y1, width, height = results[0]['box']
	x2, y2 = x1 + width, y1 + height
	# extract the face
	face = pixels[y1:y2, x1:x2]
	# resize pixels to the model size
	image = Image.fromarray(face)
	image = image.resize(required_size)
	face_array = np.asarray(image)
	print('Progress................... '+str(var)+'%')
	var = var + 4
	return face_array


json_file = open('C:\\Users\\dell\\Documents\\python\\Kiran\\model.json', 'r')
model_json = json_file.read()
json_file.close()
model = model_from_json(model_json)
model.load_weights('C:\\Users\\dell\\Documents\\python\\Kiran\\vggface.h5', True)
print('Progress................... 20%')

# extract faces and calculate face embeddings for a list of photo files
def get_embeddings(filenames):
	# extract faces
	faces = [extract_face(f) for f in filenames]
	# convert into an array of samples
	samples = np.asarray(faces, 'float32')
	print('Progress................... 70%')
	# prepare the face for the model, e.g. center pixels
	samples = preprocess_input(samples, version=2)
	# perform prediction
	yhat = model.predict(samples)
	return yhat

# determine if a candidate face is a match for a known face
def is_match(known_embedding, candidate_embedding, thresh=0.5):
	print('Progress................... 80%')
	# calculate distance between embeddings
	score = cosine(known_embedding, candidate_embedding)
	return score

def send_message(message, photo):
    #reading image in binary format
    image_data = open(photo, 'rb').read()
    #defining obj
    msg = MIMEMultipart()     
    text = MIMEText(message)
    #add the message into obj.
    msg.attach(text)
    #converting image to mime image data
    image = MIMEImage(image_data, name=os.path.basename(photo))
    #attach image to message
    msg.attach(image)
    sender_email = "dailyfitness012@gmail.com"
    rec_email = "kirankauri012@gmail.com"
    password = "9808092089"
    #message = "Hey, this was sent using python"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    print("Login success")
    server.sendmail(sender_email, rec_email, msg.as_string())
    print("Email has been sent to ", rec_email)
    server.quit()

def write_file(data, name):
    # Convert binary data to proper format and write it on Hard Disk
    filename = 'C:\\Users\\dell\\Documents\\python\\Kiran\\photos\\'+str(name)+'.jpg'
    with open(filename, 'wb') as file:
        file.write(data)

def load_image_database():
    names = []
    try:
        #try to develop connection
        print("\n\n\n")
        print("Connecting to database..............")
        connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'rohitkauri123',
            auth_plugin='mysql_native_password',
            database = 'kirancha')

        print("Connected to database!!")

        cursor = connection.cursor()
        cursor.execute("Select * from persons")
        records = cursor.fetchall()
        print("\n\n\n")
        for record in records:
            names.append(str(record[1]))
            print("Id = ", record[0])
            print("Name = ", record[1])
            image = record[2]
            print("Loading persons image from database \n")
            write_file(image, record[1])

        print("\n\n\n")    
        cursor.close()
        connection.close()
        return names
    except Error as e:
        print("Error while connecting to mysql")
        print(e)
        return null


print('Progress................... 30%')
# define filenames
load_names = load_image_database()
filenames = ['C:\\Users\\dell\\Documents\\python\\Kiran\\photos\\This Pic.jpg',
             'C:\\Users\\dell\\Documents\\python\\Kiran\\photos\\Rohit.jpg',
             'C:\\Users\\dell\\Documents\\python\\Kiran\\photos\\kiran.jpg']

# get embeddings file filenames
embeddings = get_embeddings(filenames)
score_values = []
message = ''
print(load_names)
for i in range(len(load_names)):
    score_val = is_match(embeddings[0], embeddings[i+1])
    score_values.append(score_val)
    if(score_val < 0.5): #check the score and if <0.5 then break
        message = "\n\nHello Sir!\nYou have a visitor.\nThe visitor's name is "+load_names[i]+"\n\n"
        break
    elif(i == len(load_names)-1): #at last iteration if the embedding is less than 0.5
        message = "It is Stranger"

print('Progress................... 100%')
print(message)
send_message(message, filenames[0])
