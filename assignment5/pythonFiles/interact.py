# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import maestro
import numpy as np
import math

# initialize the camera and grab a reference to the raw camera capture 
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
#lower_yellow_bound = np.array([25, 50, 50], dtype="uint8")
#upper_yellow_bound = np.array([35, 255, 255], dtype="uint8")

MOTORS = 1
TURN = 2
BODY = 0
HEADTILT = 4
HEADTURN = 3

tango = maestro.Controller()
body = 6000
headTurn = 6000
headTilt = 5500
turn = 6000
maxMotor = 5675
maxLeftTurn = 7000
maxRightTurn = 5000
motors = 6000

#tango.setAccel(MOTORS, 1)
tango.setTarget(HEADTURN, headTurn)
tango.setTarget(HEADTILT, headTilt)
#tango.setTarget(TURN, turn) 
#tango.setTarget(BODY, body)

# allow the camera to warmup
time.sleep(1)

# capture frames from the camera
cv2.namedWindow("Robo", cv2.WINDOW_NORMAL)
cv2.moveWindow("Robo", 0, 0)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    #print(len(image), " ", len(image[1]))

    #split_image = image[150:640, 0:480]
    #blur = cv2.GaussianBlur(image, (5, 5), 1)
    #hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    #mask = cv2.inRange(hsv, lower_yellow_bound, upper_yellow_bound)
    #pic = cv2.Canny(mask, 90, 140)

    # show the frame
    #picture_1 = frame
    face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_default.xml')
    #eye_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_eye.xml')
    #height, width, depth = frame.shape 
    #picture_2 = np.zeros((height, width, 3), np.uint8)
    #picture_2[:, 0:width//2] = (30, 30, 30)      # (B, G, R)
    #picture_2[:, width//2:width] = (30, 30, 30)
    #picture_3 = cv2.subtract(picture_1, picture_2)
    #gray = cv2.cvtColor(picture_3, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(image, 1.3, 4)
    #print(faces)
    for (x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
        xcenter = x + int((w/2))
        ycenter = y + int((h/2)) 
        xdist = 320 - xcenter
        ydist = 240 - ycenter
        xabs = abs(320 - xcenter)
        yabs = abs(240 - ycenter)
        
        if((xabs > 30) or (yabs > 20)):
                if(6000 + (xabs*2) >= 6300):
                        if(xdist > 0): #turn robot left 
                                if(body < 6000): #if was previously turned other way
                                        body = 6000
                                if(body == 6000):
                                        body = 6600
                                elif(body == 6600): #already turned body, so turn machine
                                        turn = 7000
                                        tango.setTarget(MOTORS, motors)
                                        tango.setTarget(TURN, turn)
                                        time.sleep(0.5)
                                        body = 6000
                                tango.setTarget(TURN, 6000)
                                tango.setTarget(BODY, body)
                        elif(xdist < 0): # turn robot right
                                if(body > 6000): # if was previously turned other way
                                        body = 6000
                                elif(body == 6000):
                                        body = 5400
                                elif(body == 5400):
                                        turn = 5000
                                        tango.setTarget(MOTORS, motors)
                                        tango.setTarget(TURN, turn)
                                        time.sleep(0.5)
                                        body = 6000
                                tango.setTarget(TURN, 6000)
                                tango.setTarget(BODY, body)
                
                tango.setTarget(HEADTURN, 6000 + (xdist*2))
                tango.setTarget(HEADTILT, 6000 + (int(ydist*2.5)))
        area = x * y 
        print(area)
        if(area > 45000): #move forwwards
                motors = 5200
                tango.setTarget(MOTORS, motors)
                time.sleep(0.35)
        elif(area < 35000): #move backwards
                motors = 6900
                tango.setTarget(MOTORS, motors)       
                time.sleep(0.35)
        else:
                motors = 6000
                tango.setTarget(MOTORS, motors)  
        motors = 6000
        tango.setTarget(MOTORS, motors)
       
    showImage()
    

    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
            shutdown()
            break

def showImage(image):
        cv2.imshow("Robo", image)
        key = cv2.waitKey(1) & 0xFF


        #stop()
         # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

def shutdown():
        #motors = 6000
        turn = 6000
        headTilt = 6000
        #tango.setTarget(MOTORS, motors)
        tango.setTarget(TURN, turn)
        tango.setTarget(HEADTILT, headTilt)
        tango.setTarget(BODY, 6000)

def findHuman():
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                image = frame.array
                face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_default.xml')
                faces = face_cascade.detectMultiScale(image, 1.3, 4)
                if (faces != null):
                        #send msg hello human
                        centerFace()

def centerBody():
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                image = frame.array
                face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_default.xml')
                faces = face_cascade.detectMultiScale(image, 1.3, 4)
                for (x,y,w,h) in faces:
                        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
                        xcenter = x + int((w/2))
                        ycenter = y + int((h/2)) 
                        xdist = 320 - xcenter
                        ydist = 240 - ycenter
                        xabs = abs(320 - xcenter)
                        yabs = abs(240 - ycenter)
                        
                        if((xabs > 30) or (yabs > 20)):
                                if(6000 + (xabs*2) >= 6300):
                                        if(xdist > 0): #turn robot left 
                                                if(body < 6000): #if was previously turned other way
                                                        body = 6000
                                                if(body == 6000):
                                                        body = 6600
                                                elif(body == 6600): #already turned body, so turn machine
                                                        turn = 7000
                                                        tango.setTarget(MOTORS, motors)
                                                        tango.setTarget(TURN, turn)
                                                        time.sleep(0.5)
                                                        body = 6000
                                                tango.setTarget(TURN, 6000)
                                                tango.setTarget(BODY, body)
                                        elif(xdist < 0): # turn robot right
                                                if(body > 6000): # if was previously turned other way
                                                        body = 6000
                                                elif(body == 6000):
                                                        body = 5400
                                                elif(body == 5400):
                                                        turn = 5000
                                                        tango.setTarget(MOTORS, motors)
                                                        tango.setTarget(TURN, turn)
                                                        time.sleep(0.5)
                                                        body = 6000
                                                tango.setTarget(TURN, 6000)
                                                tango.setTarget(BODY, body)
                                
                                tango.setTarget(HEADTURN, 6000 + (xdist*2))
                                tango.setTarget(HEADTILT, 6000 + (int(ydist*2.5)))
                        area = x * y 
                        print(area)
                        if(area > 45000): #move forwwards
                                motors = 5200
                                tango.setTarget(MOTORS, motors)
                                time.sleep(0.35)
                        elif(area < 35000): #move backwards
                                motors = 6900
                                tango.setTarget(MOTORS, motors)       
                                time.sleep(0.35)
                        else:
                                motors = 6000
                                tango.setTarget(MOTORS, motors)  
                        motors = 6000
                        tango.setTarget(MOTORS, motors)

def centerScreen():
        tango.setTarget(HEADTURN, headTurn)
        tango.setTarget(HEADTILT, headTilt)

def centerDistance():
        pass