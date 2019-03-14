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
yellow_color_boundaries = [(0, 145, 190), (137, 255, 255)]
lower_yellow_bound = np.array([25, 50, 50], dtype="uint8")
upper_yellow_bound = np.array([32, 255, 255], dtype="uint8")

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

tango.setAccel(MOTORS, 1)
tango.setTarget(HEADTURN, headTurn)
tango.setTarget(HEADTILT, headTilt)
tango.setTarget(TURN, turn)
tango.setTarget(BODY, body)

# allow the camera to warmup
time.sleep(1)

def findCoG(img):
    white_pixels = np.argwhere(img >= 250)
    size = len(white_pixels)
    # sums = [0, 0] 
    sumX = 0
    sumY = 0
    for y, x in white_pixels:
        if y > 150:
            # sums[0] += x
            # sums[1] += y
            sumX += x
            sumY += y
        else:
            size = size - 1
    if(size > 0):
        # sums[0] = sums[0] / size
        # sums[1] = sums[1] / size
        sumX = sumX / size
        sumY = sumY / size
    else:
        return -1, -1
    return sumX, sumY

def stop():
    time.sleep(.75)
    motors = 6000
    turn = 6000
    tango.setTarget(MOTORS, motors)
    tango.setTarget(TURN, turn)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    #split_image = image[150:640, 0:480]
    blur = cv2.GaussianBlur(image, (5, 5), 1)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_yellow_bound, upper_yellow_bound)
    #pic = cv2.Canny(mask, 100, 170)
    pic = cv2.Canny(mask, 100, 50)

    x, y = findCoG(pic)
    if(x != -1 and y != -1):
       # cv2.rectangle(pic, (cog[0]-10, cog[1]-10), (cog[0]+10, cog[1]+10), 1, 8)
        cv2.rectangle(pic, (x-10, y-10), (x+10, y+10), 1, 8)
    # show the frame
    cv2.imshow("Frame", pic)
    #print(cog)

    if x == -1 and y == -1:
        motors = 6000
        turn = 6000
        tango.setTarget(MOTORS, motors)
        tango.setTarget(TURN, turn)
        print("end")
        #break
    #near the center
    elif 260 <= x <= 420:
        #move forward
        motors = 5200
        tango.setTarget(MOTORS, motors)
        print("forward")
    elif 490 > x > 420:
       #move right slightly
        turn = 5350
        tango.setTarget(TURN, turn)
        print("right slightly")
    elif x >= 490:
        #move right hard
        turn = 5000
        tango.setTarget(TURN, turn)
        print("right hard")
    elif 260 > x > 180:
         #move left slightly  
        turn = 6750
        tango.setTarget(TURN, turn)
        print("left slightly")
    elif x <= 180:
        #move left hard
        turn = 7000
        tango.setTarget(TURN, turn)
        print("left hard")

    key = cv2.waitKey(1) & 0xFF


    stop()
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
            motors = 6000
            turn = 6000
            tango.setTarget(MOTORS, motors)
            tango.setTarget(TURN, turn)
            break



