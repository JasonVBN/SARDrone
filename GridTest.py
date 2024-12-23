import math
import time

import cv2
faceCascade = cv2.CascadeClassifier('C:\SAR Drone Project\FaceDetector1\haarcascade_frontalface_default.xml')

from djitellopy import tello
from time import sleep

drone = tello.Tello()
drone.connect()
print(drone.get_battery())

drone.send_rc_control(0, 0, 0, 0)

#drone.takeoff()
#drone.move_up(20)
#drone.send_rc_control(0,0,0,20)

'''
def gridpattern(length, width, height):
    radians = (41.3/180)*math.pi
    columnSize = int(math.floor(2*math.tan(radians)*height))

    columns = math.ceil(width/columnSize)

    currentHeight = drone.get_height()
    drone.move_up(max(20, height-currentHeight))

    drone.move_right(int(math.ceil(columnSize/2)))
    for i in range(0, columns):
        if i % 2 == 0:
            if i != 0:
                drone.move_right(columnSize)
                print("moved right")
            drone.move_forward(length)
            print("moved right and forward")
        elif i % 2 == 1:
            drone.move_right(columnSize)
            drone.move_back(length)
            print("moved right and back")
'''


print("Camera starting...")
drone.streamon()
start_time = time.time()
while True:
    img = drone.get_frame_read().frame
    img = cv2.resize(img, (720,480))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(gray, 1.1, 4)

    print(faces)

    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Image",img)
    cv2.waitKey(1)

    current_time = time.time()

    # Check time - every 10 s, send command to drone
    timediff = (current_time-start_time)%10
    if timediff > 9.98 or timediff < 0.02:
        #drone.send_rc_control(0,0,0,20)
        print("10 s reached")

    # Check time - break out after 25 s
    if current_time-start_time > 35:
        break
drone.streamoff()
print("Camera stopped.")
#drone.land()

#gridpattern(200,500,200)
