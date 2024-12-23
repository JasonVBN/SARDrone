import math
import threading
import time
import datetime

import cv2
faceCascade = cv2.CascadeClassifier('C:\SAR Drone Project\FaceDetector1\haarcascade_frontalface_default.xml')
bodyCascade = cv2.CascadeClassifier('C:\SAR Drone Project\FaceDetector1\haarcascade_fullbody.xml')
upperbodyCascade = cv2.CascadeClassifier('C:\SAR Drone Project\FaceDetector1\haarcascade_upperbody.xml')


from djitellopy import tello
from time import sleep

drone = tello.Tello()
drone.connect()
print(drone.get_battery())

drone.send_rc_control(0, 0, 0, 0)

drone.streamon()

drone.takeoff()

time.sleep(2)

def moving_right(length):
    moves = math.floor(length / 500)
    mod = length % 500

    for i in range(moves):
        drone.move_right(500)
    if mod > 20:
        drone.move_right(mod)

def moving_left(length):
    moves = math.floor(length / 500)
    mod = length % 500

    for i in range(moves):
        drone.move_left(500)
    if mod > 20:
        drone.move_left(mod)

def moving_forward(length):
    moves = math.floor(length / 500)
    mod = length % 500

    for i in range(moves):
        drone.move_forward(500)

    if mod > 20:
        drone.move_forward(mod)

def moving_back(length):
    moves = math.floor(length / 500)
    mod = length % 500

    for i in range(moves):
        drone.move_back(500)
    if mod > 20:
        drone.move_back(mod)

def gridpattern(length, width, height):
    print("grid length: " + str(length))
    print("grid width: " + str(width))

    radians = (41.3/180)*math.pi
    columnSize = int(math.floor(2*math.tan(radians)*height))
    print("column size: " + str(columnSize))

    columns = math.ceil(width/columnSize)
    print("number of columns: " + str(columns))

    currentHeight = drone.get_height()

    moves_up = math.floor(height/500)
    mod = height % 500

    for i in range (moves_up):
        drone.move_up(500)
    if mod > 20:
        drone.move_up(mod)
    # drone.move_up(max(20, height-currentHeight))


   # drone.move_up(500)


    moving_right(int(math.ceil(columnSize/2)))
    for i in range(0, columns):
        if i % 2 == 0:
            if i != 0:
                #first iteration, dont move right
                moving_right(columnSize)
                print("moved right")
            moving_forward(length)
            print("moved right and forward")
        elif i % 2 == 1:
            moving_right(columnSize)
            moving_back(length)
            print("moved right and back")
    drone.land()


def video_feed():
    imgCount = 0
    while True:
        img = drone.get_frame_read().frame
        #img = cv2.resize(img, (720,480))

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # faces = faceCascade.detectMultiScale(gray, 1.1, 4)
        # bodies = bodyCascade.detectMultiScale(gray, 1.1, 4)
        upperbodies = upperbodyCascade.detectMultiScale(gray, 1.1, 4)

        for (x,y,w,h) in upperbodies:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow("Image",img)

        currentTime = datetime.datetime.now()
        # print(currentTime)
        timeStr = currentTime.strftime("%Y%m%d_%H%M%S%f")
        # imgNum = str(imgCount)
        # imgNum = imgNum.rjust(4, '0')
        fileName = "Dec23Run2/img" + timeStr + ".jpg"
        print("Image " + str(imgCount) + " saved as: " + fileName)
        cv2.imwrite(fileName, img)
        imgCount += 1

        cv2.waitKey(1)


t1 = threading.Thread(target=gridpattern, args=(300,500,250,))
t2 = threading.Thread(target=video_feed)

t1.start()
t2.start()

t1.join()
t2.join()

drone.streamoff()
print("Camera stopped.")
drone.land()

#gridpattern(200,500,200)
