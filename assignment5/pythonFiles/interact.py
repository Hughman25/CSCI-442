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
temp = 0
i = 0


#Assign values to motors
tango.setTarget(HEADTURN, headTurn)
tango.setTarget(HEADTILT, headTilt)
#tango.setTarget(TURN, turn) 
#tango.setTarget(BODY, body)
#
# allow the camera to warmup
time.sleep(1)

#Set timer variables
start_time = 0.0
bodyFlag = True
distFlag = True
time_flag = True
findHumanFlag = True


# capture frames from the camera
cv2.namedWindow("Robo", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Robo", 800, 400)
cv2.moveWindow("Robo", 0, 0)

def shutdown():
        #motors = 6000
        turn = 6000
        headTilt = 6000
        #tango.setTarget(MOTORS, motors)
        tango.setTarget(TURN, turn)
        tango.setTarget(HEADTILT, headTilt)
        tango.setTarget(BODY, 6000)
        client.client.killSocket()


def nextSearchPosition():
        positions = [(6000, 6000, 6000), (6000, 7000, 6500), (6800, 7000, 6500), (6000, 7000, 6500), (5200, 7000, 6500), (6000, 6000, 6000),
                        (5200, 5000, 5500), (6000, 5000, 5500), (6800, 5000, 5500)] #tilt, turn, bodyturn
        global headTilt, headTurn, i
        headTilt = positions[i][0]
        headTurn = positions[i][1]
        tango.setTarget(HEADTURN, headTurn)
        tango.setTarget(HEADTILT, headTilt)
        tango.setTarget(BODY, positions[i][2])
        time.sleep(1)
        i = i + 1
        if(i == 9):
                i = 0
                

def centerBody(xabs, yabs, xdist):
        global body, motors, turn, bodyFlag, headTilt, headTurn

        if(headTurn == 5000):
                body = 5400
                turn = 5000
                tango.setTarget(MOTORS, motors)
                tango.setTarget(TURN, turn)
                time.sleep(.8)

        elif(headTurn == 7000):
                body = 6600
                turn = 7000
                tango.setTarget(MOTORS, motors)
                tango.setTarget(TURN, turn)
                time.sleep(.8)  
        elif(xabs > 75):
                if(xdist > 0): #turn robot left 
                        if(body < 6000): #if was previously turned other way
                                body = 6000
                        if(body == 6000):
                                body = 6600
                        if(body == 6600): #already turned body, so turn machine
                                turn = 7000
                                #tango.setTarget(MOTORS, motors)
                                tango.setTarget(TURN, turn)
                                time.sleep(0.5)
                                body = 6000
                elif(xdist < 0): # turn robot right
                        if(body > 6000): # if was previously turned other way
                                body = 6000
                        if(body == 6000):
                                body = 5550
                        if(body == 5550):
                                turn = 5000
                                tango.setTarget(MOTORS, motors)
                                tango.setTarget(TURN, turn)
                                time.sleep(0.5)
                                body = 6000

        bodyFlag = False
        tango.setTarget(TURN, 6000)
        tango.setTarget(BODY, 6000)
        tango.setTarget(HEADTURN, 6000)
        
def centerScreen(xabs, yabs, xdist, ydist):
        
        if((xabs > 60) or (yabs > 50)):
                xdist = xdist + int(xdist*.3)
                ydist = ydist + int(ydist*.3)
                tango.setTarget(HEADTURN, 6000 + (xdist*2))
                tango.setTarget(HEADTILT, 6000 + (int(ydist*2.5)))
        elif((xabs < 60) and (yabs > 50)):
                return True
        return False
        


def startTimer():
        global start_time
        start_time = time.time()
        
def checkTimer(time_bool):
        global start_time, time_flag, findHumanFlag, bodyFlag, distFlag
        if(time_bool):
                if(time.time() - start_time > 8):
                        findHumanFlag = True
                        bodyFlag = True
                        distFlag = True
        else:
                start_time = 0
                time_flag = True

nextSearchPosition()
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    
        # grab the raw NumPy array representing the image
        image = frame.array

        face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(image, 1.3, 4)
        if(len(faces) != 0):
                if(findHumanFlag):
                        client.client.sendData("Hello Human")
                        findHumanFlag = False
                checkTimer(False)
                x,y,w,h = faces[0]
                cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
                xcenter = x + int((w/2))
                ycenter = y + int((h/2)) 
                xdist = 320 - xcenter
                ydist = 240 - ycenter
                xabs = abs(320 - xcenter)
                yabs = abs(240 - ycenter)

                if(bodyFlag):
                        centerBody(xabs, yabs, xdist)
                else:
                        centerScreen(xabs, yabs, xdist, ydist)
                        if(distFlag):
                                if(w*h < 19000 or w*h > 24000):
                                        if(w*h < 19000): #move forwwards
                                                temp = (19000-w*h) / 5800
                                                motors = 5200
                                                tango.setTarget(MOTORS, motors)
                                                time.sleep(temp)
                                        elif(w*h > 24000): #move backwards
                                                temp = (w*h-24000)/50000
                                                motors = 6900
                                                tango.setTarget(MOTORS, motors)       
                                                time.sleep(temp)
                                        distFlag = False
                                        motors = 6000
                                        tango.setTarget(MOTORS, motors)
                                if(centerScreen(xabs, yabs, xdist, ydist)):
                                        print("Found you human")
        else:
                if(time_flag):
                        startTimer()
                        time_flag = False
                else:
                        checkTimer(True)
                        if(findHumanFlag):
                                nextSearchPosition()

        cv2.imshow("Robo", image)
        key = cv2.waitKey(1) & 0xFF
        #stop()
         # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
                shutdown()
                break
