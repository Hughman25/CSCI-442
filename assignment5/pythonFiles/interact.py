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
body = 5700
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
#time.sleep(1)
height = 480
width = 640
hCenter = 480/2
wCenter = 640/2
#top left quadrant
htopLeftMin = 0
wtopLeftMin = 0
htopLeftMax = hCenter/2
wtopLeftMax = wCenter/2
#top right quadrant
htopRightMin = 0
wtopRightMin = wCenter
htopRightMax = hCenter
wtopRightMax = 640
#bottom left quadrant
hbotLeftMin = hCenter
wbotLeftMin = 0
hbotLeftMax = height
wbotLeftMax = wCenter
#bottom right Quadrant
hbotRightMin = hCenter
wbotRightMin = wCenter
hbotRightMax = height
wbotRightMax = width

# capture frames from the camera
cv2.namedWindow("Robo", cv2.WINDOW_NORMAL)
cv2.moveWindow("Robo", 0, 0)
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    print(len(image), " ", len(image[1]))

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
        #print("x", xcenter, ": y", ycenter)
        xabs = abs(320 - xcenter)
        yabs = abs(240 - ycenter)
        
        if((xabs > 30) or (yabs > 20)):
                if(6000 + (xabs*2) > 7500):
                        pass
                tango.setTarget(HEADTURN, 6000 + (xdist*2))
                tango.setTarget(HEADTILT, 6000 + (int(ydist*2.5)))
                print(xdist, " ", ydist)
                '''
                if(xabs > 0 and yabs > 0): # top left
                        hspeed = int((320 - xcenter)/2) #head movement speed horizontle
                        vspeed = int((240 - ycenter)/2) #verticle
                        tango.setTarget(HEADTURN, 6000 + hspeed)
                        tango.setTarget(HEADTILT, 6000 + vspeed)
                elif(xabs > 0 and yabs < 0): # bottom left
                        pass
                elif(xabs < 0 and yabs > 0): # top right
                        pass
                elif(xabs < 0 and yabs < 0): # bottom right
                        pass
                '''
        '''
        if(xcenter < 285 and ycenter < 205): #top left
                hspeed = int((320 - xcenter)/2) #head movement speed horizontle
                vspeed = int((240 - ycenter)/2) #verticle
                tango.setTarget(HEADTURN, 6000 + hspeed)
                tango.setTarget(HEADTILT, 6000 + vspeed)

        elif(xcenter > 355 and ycenter < 205):#bottom left
                hspeed = int((320 + xcenter)/2) #head movement speeds
                vspeed = int((240 - ycenter)/2) #
                tango.setTarget(HEADTURN, 6000 - hspeed)
                tango.setTarget(HEADTILT, 6000 + vspeed)

        elif(xcenter < 285 and ycenter > 275):#top right
                hspeed = int((320 - xcenter)/2)  #head movement speeds
                vspeed = int((240 + ycenter)/2) #
                tango.setTarget(HEADTURN, 6000 - hspeed)
                tango.setTarget(HEADTILT, 6000 + vspeed)

        elif(xcenter > 355 and ycenter > 275):#bottom right
                hspeed = int((320 + xcenter)/2)  #head movement speeds
                vspeed = int((240 + ycenter)/2) #
                tango.setTarget(HEADTURN, 6000 - hspeed)
                tango.setTarget(HEADTILT, 6000 - vspeed)
        '''
        #roi_gray = gray[y:y+h, x:x+w]
        #roi_color = picture_3[y:y+h, x:x+w]
        #eyes = eye_cascade.detectMultiScale(roi_gray)
        #for (ex,ey,ew,eh) in eyes:
            #cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        #cv2.imshow("Robo", image)
    #cv2.rectangle(image,(285,205), (355, 275), (255,0,0, 2))
    cv2.imshow("Robo", image)
    

    key = cv2.waitKey(1) & 0xFF


    #stop()
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
            #motors = 6000
            turn = 6000
            headTilt = 6000
            #tango.setTarget(MOTORS, motors)
            tango.setTarget(TURN, turn)
            tango.setTarget(HEADTILT, headTilt)
            break



