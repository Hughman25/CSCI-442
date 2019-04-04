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
start_time = 0
bodyFlag = True
distFlag = True
time_flag = True


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
        # headTilt = 6000
        global bodyFlag, distFlag
        bodyFlag = True
        distFlag = True
        positions = [(6000, 6000), (6000, 7000), (7000, 7000), (7000, 5000), (6000, 5000)] #tilt, turn
        global headTilt, headTurn, i
        # headTurn = 6000
        if (len(faces) != 0):
                print("FOUND")
                client.client.sendData("Hello Human")
                return True
        else:
                
                tango.setTarget(HEADTURN, positions[i][1])
                tango.setTarget(HEADTILT, positions[i][0])
                time.sleep(0.5)
                i = i + 1
                if(i == 5):
                        i = 0
                return False
        

                

def centerBody(xabs, yabs, xdist):
        global body, motors, turn, bodyFlag
                
        if((xabs > 100) or (yabs > 100)):
                if(xdist > 0): #turn robot left 
                        if(body < 6000): #if was previously turned other way
                                body = 6000
                        if(body == 6000):
                                body = 6500
                        elif(body == 6600): #already turned body, so turn machine
                                turn = 7000
                                #tango.setTarget(MOTORS, motors)
                                tango.setTarget(TURN, turn)
                                time.sleep(0.5)
                                body = 6000
                        tango.setTarget(TURN, 6000)
                        tango.setTarget(BODY, body)
                elif(xdist < 0): # turn robot right
                        if(body > 6000): # if was previously turned other way
                                body = 6000
                        elif(body == 6000):
                                body = 5550
                        elif(body == 5400):
                                turn = 5000
                                tango.setTarget(MOTORS, motors)
                                tango.setTarget(TURN, turn)
                                time.sleep(0.5)
                                body = 6000
                        tango.setTarget(TURN, 6000)
                        tango.setTarget(BODY, body)
                tango.setTarget(HEADTURN, 6000)
                tango.setTarget(HEADTILT, 6000)
        else:
                print("TEST1")
                bodyFlag = False
        
def centerScreen(xabs, yabs, xdist, ydist):
        tango.setTarget(HEADTURN, 6000)
        tango.setTarget(HEADTILT, 6000)
        
        if((xabs > 50) or (yabs > 40)):
                tango.setTarget(HEADTURN, 6000 + (xdist*2))
                tango.setTarget(HEADTILT, 6000 + (int(ydist*2.5)))
        elif((xabs < 50) and (yabs > 40)):
                return True
        return False
        
def centerDistance(x, y):
        global distFlag
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
        distFlag = False


def startTimer():
        start_time = time.time
        
def checkTimer(time_bool):
        global start_time, time_flag
        if(time_bool):
                if(time.time - start_time > 4):
                        findHuman()
        else:
                start_time = 0
                time_flag = True

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    
        # grab the raw NumPy array representing the image
        image = frame.array

        face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(image, 1.3, 4)

        if(findHuman(faces)):
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
                                centerDistance(x, y)
                                if(centerScreen(xabs, yabs, xdist, ydist)):
                                        print("Found you human")
        else:
                if(time_flag):
                        startTimer()
                        time_flag = False
                else:
                        checkTimer(True)

        showImage(image)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
                shutdown()
                break
