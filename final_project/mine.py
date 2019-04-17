from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import maestro
import numpy as np
import client

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640,480))

#Set motor enums
BODY = 0
MOTORS = 1
TURN = 2
HEADTURN = 3
HEADTILT = 4 
#set arm motors

#Set default motor values
tango = maestro.Controller()
body = 6000
headTurn = 6000
headTilt = 6000
turn = 6000
maxMotor = 5675
maxLeftTurn = 7000
maxRightTurn = 5000
motors = 6000
#set arm motors

#Assign values to motors
tango.setTarget(HEADTURN, headTurn)
tango.setTarget(HEADTILT, headTilt)
tango.setTarget(TURN, turn) 
tango.setTarget(BODY, body)
#set arm targets

#Stage booleans
init_stage_b = False #Turns false after passing Yellow Line
stage_one_b = False #Turns to True after passing Yellow line, false after Blue Line
stage_two_b = False #True after Blue Line, False after obtaining ice from Human
stage_three_b = False #True after obtaining Ice, False after passing Blue Line
stage_four_b = False #True after passing Blue Line, False after passing Yellow
final_stage_b = False #True after passing Yellow Line. False after completion.

# capture frames from the camera


#values for finding orange line with hsv
lower_yellow_bound = np.array([25, 50, 50], dtype="uint8")
upper_yellow_bound = np.array([35, 255, 255], dtype="uint8")
lower_blue_bound = np.array([30, 100, 100], dtype="uint8") #37, 51, 255
upper_blue_bound = np.array([47, 255, 255], dtype="uint8")

time.sleep(2)
def getFrame():
    '''
    camera.start_preview()
    # Camera warm-up time
    time.sleep(2)
    frame = camera.capture(rawCapture, format="bgr", use_video_port=True)
    image = frame.array
    '''
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        break
    return image
 
def showFrame(image):
    cv2.imshow("Main Camera", image)
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


#function to determine center of gravity
def findCoG(img):
    white_pixels = np.argwhere(img >= 250)
    size = len(white_pixels)
    sumX = 0
    sumY = 0
    for y, x in white_pixels:
        if y > 175:
            sumX += x
            sumY += y
        else:
            size = size - 1
    if(size > 0):
        sumX = sumX / size
        sumY = sumY / size
    else:
        return -1, -1
    return sumX, sumY



def init_stage():
    global init_stage_b
    headTilt = 4000
    tango.setTarget(HEADTILT, headTilt)
    while(True):
       
        image = getFrame()
        blur = cv2.GaussianBlur(image, (5, 5), 1)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_yellow_bound, upper_yellow_bound)
        pic = cv2.Canny(mask, 100, 50)
        x, y = findCoG(pic)
        showFrame(pic)
        if x == -1 and y == -1:
            motors = 5500
            tango.setTarget(MOTORS, motors)
            time.sleep(.5)
            motors = 6000
            turn = 6000
            tango.setTarget(MOTORS, motors)
            tango.setTarget(TURN, turn)
            init_stage_b = True
        #near the center
        elif 280 <= x <= 400:
            turn = 6000
            tango.setTarget(TURN, turn)
            motors -= 10
            if(motors > maxMotor):
                motors = maxMotor
            tango.setTarget(MOTORS, motors)
            print("forward")
        elif 490 > x > 400:
            motors = 6000
            tango.setTarget(MOTORS, motors)
            turn -= 25
            if(turn < maxRightTurn):
                turn = maxRightTurn
            tango.setTarget(TURN, turn)
            print("right slightly")
        elif x >= 490:
            motors = 6000
            tango.setTarget(MOTORS, motors)
            turn -= 25
            if(turn < maxRightTurn):
                turn = maxRightTurn
            tango.setTarget(TURN, turn)
            print("right hard")
        elif 280 > x > 180:
            motors = 6000
            tango.setTarget(MOTORS, motors)
            turn += 25
            if(turn > maxLeftTurn):
                turn = maxLeftTurn
            tango.setTarget(TURN, turn)
            print("left slightly")
        elif x <= 180:
            motors = 6000
            tango.setTarget(MOTORS, motors)
            turn += 25
            if(turn > maxLeftTurn):
                turn = maxLeftTurn
            tango.setTarget(TURN, turn)
            print("left hard")
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



def stage_one():
    pass

def stage_two():
    pass

def stage_three():
    pass

def stage_four():
    pass

def final_stage():
    pass
 

def main():
    print("Never")
    init_stage()
    stage_one()
    stage_two()
    stage_three()
    stage_four()
    final_stage()

print("B4 main() call")
main()