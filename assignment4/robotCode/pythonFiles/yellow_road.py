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
yellow_color_boundaries = [(0, 200, 200), (137, 255, 255)]
lower_yellow_bound = np.array(yellow_color_boundaries[0], dtype="uint8")
upper_yellow_bound = np.array(yellow_color_boundaries[1], dtype="uint8")

MOTORS = 1
TURN = 2
BODY = 0
HEADTILT = 4
HEADTURN = 3

tango = maestro.Controller()
body = 6000
headTurn = 6000
headTilt = 1600
turn = 6000

tango.setAccel(MOTORS, 1)
tango.setTarget(HEADTURN, headTurn)
tango.setTarget(HEADTILT, headTilt)
tango.setTarget(TURN, turn)
tango.setTarget(BODY, body)

# allow the camera to warmup
time.sleep(0.1)
def findCoG(img):
    white_pixels = np.argwhere(img >= 200)
    size = len(white_pixels)
    sumX = 0
    sumY = 0
    for x, y in white_pixels:
        sumX += x
        sumY += y
    sumX = sumX / size
    sumY = sumY / size
    return (x, y)


# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    mask = cv2.inRange(image, lower_yellow_bound, upper_yellow_bound)
    pic = cv2.Canny(mask, 100, 170)
    #pic = cv2.Canny(image, 100, 170)

    cog = findCoG(pic)
    cv2.rectangle(pic, (cog[0]+10, cog[1]+10), (cog[0]-10, cog[1]-10), (255,0,0), 1, 8)
    # show the frame
    cv2.imshow("Frame", pic)
    if cog[1] < 160:
        motors = 6000
        turn = 6000
        tango.setTarget(MOTORS, motors)
        tango.setTarget(TURN, turn)
        break
    #near the center
    elif 330 < cog[0] > 310:
        #move forward
        motors = 6600
        tango.setTarget(MOTORS, motors)
    elif 400 > cog[0] > 330:
        #move left slightly
        turn = 2600
        tango.setTarget(TURN, turn)
    elif cog[0] > 400:
        #move left hard
        turn = 2110
        tango.setTarget(TURN, turn)
    elif 260 < cog[0] > 310:
        #move right slightly
        turn = 6600
        tango.setTarget(TURN, turn)
    elif cog[0] < 260:
        #move right hard
        turn = 7000
        tango.setTarget(TURN, turn)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
            motors = 6000
            turn = 6000
            tango.setTarget(MOTORS, motors)
            tango.setTarget(TURN, turn)
            break



