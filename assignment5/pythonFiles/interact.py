# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import maestro
import numpy as np
import client

# initialize the camera and grab a reference to the raw camera capture 
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480)) 

#Set motor enums
MOTORS = 1
TURN = 2
BODY = 0
HEADTILT = 4
HEADTURN = 3

#Set motor values
tango = maestro.Controller()
body = 6000
headTurn = 6000
headTilt = 6000
turn = 6000
maxMotor = 5675
maxLeftTurn = 7000
maxRightTurn = 5000
motors = 6000
tCounter = 0
hCounter = 0
rtf = True #rotate turn forwards
rtb = False #rotate tback
tff = True #tilt face forward
tfb = False# tilt face back
temp = 0


#Assign values to motors
tango.setTarget(HEADTURN, headTurn)
tango.setTarget(HEADTILT, headTilt)
#tango.setTarget(TURN, turn) 
#tango.setTarget(BODY, body)
#
# allow the camera to warmup
#time.sleep(1)

#Set timer variables
start_time = 0
flag = True

# capture frames from the camera
cv2.namedWindow("Robo", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Robo", 800, 400)
cv2.moveWindow("Robo", 0, 0)
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
        client.client.killSocket()
def findHuman(faces):
        flag = True
        # headTilt = 6000
        # headTurn = 6000
        if (len(faces) != 0):
                print("FOUND")
                client.client.sendData("Hello Human")
                return True
        else:
                if(headTilt == 6000 and headTurn == 6000):
                        headTurn = 7000
                elif(headTilt == 6000 and headTurn == 7000):
                        headTilt = 7000
                elif(headTilt == 7000 and headTurn == 7000):
                        headTurn = 5000
                elif(headTilt == 7000 and headTurn == 5000):
                        headTilt = 5000
                elif(headTilt == 5000 and headTurn == 5000):
                        headTurn == 7000
                
                tango.setTarget(HEADTURN, headTurn)
                tango.setTarget(HEADTILT, headTilt)

                return False
        
        #centerBody(image, faces)

                

def centerBody(xabs, yabs, xdist):
       # for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        #image = frame.array
        #ace_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_default.xml')
        #faces = face_cascade.detectMultiScale(image, 1.3, 4)
       # checkFaces(faces)
        # for (x,y,w,h) in faces:
        #         cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
        #         xcenter = x + int((w/2))
        #         ycenter = y + int((h/2)) 
        #         xdist = 320 - xcenter
        #         ydist = 240 - ycenter
        #         xabs = abs(320 - xcenter)
        #         yabs = abs(240 - ycenter)
                
        if((xabs > 30) or (yabs > 20)):
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
                return True
        else:
                print("TEST1")
                return True
        
def centerScreen(xabs, yabs, xdist, ydist):
        tango.setTarget(HEADTURN, headTurn)
        tango.setTarget(HEADTILT, headTilt)
        
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                image = frame.array
                face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_default.xml')
                faces = face_cascade.detectMultiScale(image, 1.3, 4)
                checkFaces(faces)
                for (x,y,w,h) in faces:
                        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
                        xcenter = x + int((w/2))
                        ycenter = y + int((h/2)) 
                        xdist = 320 - xcenter
                        ydist = 240 - ycenter
                        xabs = abs(320 - xcenter)
                        yabs = abs(240 - ycenter)
                        if((xabs > 30) or (yabs > 20)):
                                tango.setTarget(HEADTURN, 6000 + (xdist*2))
                                tango.setTarget(HEADTILT, 6000 + (int(ydist*2.5)))
                        elif((xabs < 30) and (yabs > 20)):
                                if(flag):
                                        return True
                        return False
        
def centerDistance(x, y):
        area = x * y 
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
                centerScreen()
        motors = 6000
        tango.setTarget(MOTORS, motors)

def checkFaces(faces):
        if(len(faces) != 0):
                startTimer()
                checkTimer(True)
        else:
                checkTimer(False)

def startTimer():
        start_time = time.time
        
def checkTimer(time_bool):
        if(time_bool):
                if(time.time - start_time > 4):
                        findHuman()
        else:
                start_time = 0

#findHuman()

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    
        # grab the raw NumPy array representing the image
        image = frame.array

        face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(image, 1.3, 4)

        if(findHuman(faces)):
                for (x,y,w,h) in faces:
                        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
                        xcenter = x + int((w/2))
                        ycenter = y + int((h/2)) 
                        xdist = 320 - xcenter
                        ydist = 240 - ycenter
                        xabs = abs(320 - xcenter)
                        yabs = abs(240 - ycenter)

                        if(centerBody(xabs, yabs, xdist)):
                                if(centerScreen(xabs, yabs, xdist, ydist)):
                                        if(centerDistance(x, y)):
                                                if(centerScreen(xabs, yabs, xdist, ydist)):
                                                        print("Found you human")
                                                else:
                                                        print("Failed 2nd centerScreen")
                                        else:
                                                print("Failed centerDistance")
                                else:
                                        print("Failed centerScreen")
                        else:
                                print("Failed centerbody")
        else:
                print("FAiled findHuman")
                '''
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
                
        rtf = True #rotate turn forwards
        rtb = False #rotate tback
        tff = True #tilt face forward
        tfb = False# tilt face back
    else:# scan for faces
        print("hi")
        if(headTilt <= 7200 and tff == True):
                headTilt = headTilt + 1
        else:
                ttf = False
                tfb = True
        if(headTilt >= 2500 and tfb == True):
                headTilt = headTilt - 1
        else:
                tfb = False
                ttf = True

        if(headTurn <= 7200 and rtf == True):
                headTurn = headTurn + 1
        else:
                rtf = False
                rtb = True

        if(headTurn >= 2500 and rtb == True):
                headTurn = headTurn - 1
        else:
                rtb = False
                rtf = True
        
        tango.setTarget(HEADTURN, headTurn)
        tango.setTarget(HEADTILT, headTilt)
        '''
        showImage(image)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
                shutdown()
                break
