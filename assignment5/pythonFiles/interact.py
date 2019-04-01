# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import maestro
import numpy as np

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
headTilt = 1200
turn = 6000
maxMotor = 5675
maxLeftTurn = 7000
maxRightTurn = 5000
motors = 6000

tango.setAccel(MOTORS, 1)
tango.setTarget(HEADTURN, headTurn)
tango.setTarget(HEADTILT, headTilt)
tango.setTarget(TURN, turn)
tango.setTarget(BODY, body)

# allow the camera to warmup
time.sleep(1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    #split_image = image[150:640, 0:480]
    blur = cv2.GaussianBlur(image, (5, 5), 1)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_yellow_bound, upper_yellow_bound)
    pic = cv2.Canny(mask, 90, 140)

    # show the frame
    cv2.imshow("Frame", pic)
 

    key = cv2.waitKey(1) & 0xFF


    #stop()
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
            stop()
            break



