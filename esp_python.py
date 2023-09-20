import urllib.request
import http
from time import sleep
import face_recognition
import cv2
from time import sleep
from openpyxl import Workbook
import datetime
import csv
import json
import time
import os
import urllib.request
import time
import os
import serial
base = "http://192.168.43.157/"
name=""
xyu=""
top = 4
right = 4
bottom = 4
left = 4

image_1 = face_recognition.load_image_file("Iswarya.jpeg")
image_1_face_encoding = face_recognition.face_encodings(image_1)[0]
image_2 = face_recognition.load_image_file("Anju.jpg")
image_2_face_encoding = face_recognition.face_encodings(image_2)[0]

known_face_encodings = [
    image_1_face_encoding,
    image_2_face_encoding
    ]
known_face_names = ["Iswarya","Anju"]
face_locations = []
face_encodings = []
face_names = []
video_capture = cv2.VideoCapture(0)
first_match_index="9"
gy=0
facei=0
while True:
	process_this_frame = True
	ret, frame = video_capture.read()
	small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
	rgb_small_frame = small_frame[:, :, ::-1]
	name=""
	if process_this_frame:
		face_locations = face_recognition.face_locations(rgb_small_frame)
		face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
		print(len(face_encodings))
		first_match_index=9
		for face_encoding in face_encodings:
		    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
		    name = "Unknown"
		    cv2.imwrite("temp.jpg",frame)
		    if True in matches:
		        first_match_index = matches.index(True)
		        print(first_match_index)
		        name = known_face_names[first_match_index]
		    face_names.append(name)
		    process_this_frame = not process_this_frame
		    for (top, right, bottom, left), name in zip(face_locations, face_names):
		        top *= 4
		        right *= 4
		        bottom *= 4
		        left *= 4
		cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
		cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
		font = cv2.FONT_HERSHEY_DUPLEX
		cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
	cv2.imshow('Video', frame)
	face_names=[]
	ft=str(first_match_index)
	#print(name)
	if "Unknown" in name:
	    facei=0
	    os.system("python mail.py")
	elif "Iswarya" in name:
	    facei=1
	elif "Anju" in name:
	    facei=2
	gy=gy+1
	if gy>25:
	    break
	cv2.waitKey(1)
video_capture.release()
cv2.destroyAllWindows()
def transfer(my_url):   #use to send and receive data
    try:
        n = urllib.request.urlopen(base + my_url).read()
        n = n.decode("utf-8")
        return n

    except http.client.HTTPException as e:
        return e

   #Send this data
g=""
h=""
r=""
ft=""
re=[]*2
k=0
res=""
while True:
    two = transfer(str(res))
    #print(two)
    r=str(two)
    print(r)
    sleep(1)
    k=k+1
    it=0
    re=[]
    if k>1:
        for ty in r:
            try:
                if '-' not in ty:
                    ft=ft+str(ty)
                else:
                    x=float(ft)
                    print(it)
                    re.append(x)
                    ft=""
                    it=it+1
                    if it==2:
                        break
            except:
                print("pass")
        ft=""
        print("TEMPERATURE")
        print(re[0])
        print("LDR")
        print(re[1])
        import pickle
        filename = 'knnfan.sav'
        loaded_model = pickle.load(open(filename, 'rb'))
        a=float(re[0])
        b=float(re[1])
        Current_reports = [[facei,b,a]]
        predicted = loaded_model.predict(Current_reports)
        print(predicted[0])
        h=str(predicted[0])
        import pickle
        filename = 'knnlight.sav'
        loaded_model = pickle.load(open(filename, 'rb'))
        a=float(re[0])
        b=float(re[1])
        Current_reports = [[facei,b,a]]
        predicted = loaded_model.predict(Current_reports)
        print(predicted[0])
        g=str(4-int(predicted[0]))

        res=g+h


    