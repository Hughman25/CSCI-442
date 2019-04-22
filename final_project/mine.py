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
SHOULDER = 6
HAND = 11

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
shoulder = 6000
hand = 6000

#Assign values to motors
tango.setTarget(HEADTURN, headTurn)
tango.setTarget(HEADTILT, headTilt)
tango.setTarget(TURN, turn)
tango.setTarget(BODY, body)
tango.setTarget(SHOULDER, shoulder)
tango.setTarget(HAND, hand)
#set arm targets


#values for finding orange line with hsv
lower_yellow_bound = np.array([20, 50, 50], dtype="uint8")
upper_yellow_bound = np.array([39, 255, 255], dtype="uint8")
lower_pink_bound = np.array([125, 35, 100], dtype="uint8") #37, 51, 255
upper_pink_bound = np.array([180, 125, 125], dtype="uint8")
lower_white_bound = np.array([0, 0, 240], dtype="uint8")
upper_white_bound = np.array([255, 15, 255], dtype="uint8")
lower_green_bound = np.array([50, 50, 50], dtype="uint8")
upper_green_bound = np.array([70, 255, 255], dtype="uint8")


time.sleep(2)
def getFrame(stage):
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        if stage == 0:
            blur = cv2.GaussianBlur(image, (5, 5), 1)
            hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower_yellow_bound, upper_yellow_bound)
            image = cv2.Canny(mask, 100, 50)
        elif stage == 1:
            blur = cv2.GaussianBlur(image, (5, 5), 1)
            hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower_pink_bound, upper_pink_bound)
            image = cv2.Canny(mask, 100, 50)
        elif stage == 2:
            blur = cv2.GaussianBlur(image, (5, 5), 1)
            hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower_white_bound, upper_white_bound)
            image = cv2.Canny(mask, 100, 50)
        elif stage == 3:
            blur = cv2.GaussianBlur(image, (5, 5), 1)
            hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower_green_bound, upper_green_bound)
            image = cv2.Canny(mask, 100, 50)
        break
    return image


def showFrame(image):
    cv2.imshow("Main Camera", image)


def shutdown():
    motors = 6000
    turn = 6000
    headTilt = 6000
    tango.setTarget(MOTORS, motors)
    tango.setTarget(TURN, turn)
    tango.setTarget(HEADTILT, headTilt)
    tango.setTarget(BODY, 6000)
    tango.setTarget(HAND, 6000)
    tango.setTarget(SHOULDER, 6000)
    client.client.killSocket()
    quit()

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


def orientate(flip):
    if(flip):
        tango.setTarget(TURN, 5500)
        time.sleep(.3)
        tango.setTarget(MOTORS, 5600)
        time.sleep(.3)
        tango.setTarget(MOTORS, 6000)
        tango.setTarget(TURN, 6800)
        time.sleep(.5)
    elif(not flip):
        tango.setTarget(TURN, 6500)
        time.sleep(.3)
        tango.setTarget(MOTORS, 5600)
        time.sleep(.3)
        tango.setTarget(MOTORS, 6000)
        tango.setTarget(TURN, 5200)
        time.sleep(.5)


def findHighestY(img):
   white_pixels = np.argwhere(img >= 254)
   highest_y = 0
   for y, x in white_pixels:
       if y > highest_y:
           highest_y = y
   return highest_y


def avoidWhite():
    #avoid rocks
    img = getFrame(2)
    #showFrame(img)
    high_y = findHighestY(img)
    x, y = findCoG(img)
    if high_y >= 410 and 380 > x > 260:
        print("backwards")
        tango.setTarget(MOTORS, 6800)
        time.sleep(0.4)
    if 315 > x > 180:
        print("right turn")
        tango.setTarget(TURN, 5200)
        time.sleep(.75)
        tango.setTarget(TURN, 6000)
    elif 490 > x > 325:
        print("left turn")
        tango.setTarget(TURN, 6800)
        time.sleep(.75)
        tango.setTarget(TURN, 6000)
    rawCapture.truncate(0)
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        shutdown()
        return 1


#function to determine center of gravity
def findCoG(img):
    white_pixels = np.argwhere(img >= 254)
    size = len(white_pixels)
    sumX = 0
    sumY = 0
    if(size < 200):
        return -1, -1
    for y, x in white_pixels:
        if y > 100:
            sumX += x
            sumY += y
    if(size > 0):
        sumX = sumX / size
        sumY = sumY / size
    else:
        return -1, -1
    return sumX, sumY

def findCenterWhitePixels(img):
    white_pixels = np.argwhere(img >= 254)
    count = 0
    for y, x in white_pixels:
        if y > 180:
            if 350 > x > 290:
                count += 1
    if count > 50:
        return 1
    else:
        return 0


def threshold():
    img = getFrame(2)
    white_pixels = np.argwhere(img >= 254)
    size = len(white_pixels)
    print(size)
    rawCapture.truncate(0)
    if size < 1700:
        if findCenterWhitePixels(img):
            return 1
        return 0
    else:
        return 1

def findIce():
   pass

#Find yellow line and cross it
def init_stage():
    headTilt = 4000
    tango.setTarget(HEADTILT, headTilt)
    tango.setTarget(TURN, 7000)
    flag = False

    while True:
        img = getFrame(0)
        showFrame(img)
        x, y = findCoG(img)

        if 300 <= x <= 380:
            print("Forward ini")
            #go forward toward the line
            tango.setTarget(TURN, 6000)
            tango.setTarget(MOTORS, 5200)
            flag = True

        if y > 400 and flag:
            time.sleep(.8)
            tango.setTarget(MOTORS, 6000)
            client.client.sendData("Crossed the Line")
            rawCapture.truncate(0)
            break

        rawCapture.truncate(0)
        if threshold() and flag:
            if avoidWhite():
                break

        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
                shutdown()
                break


    #Avoid rocks, find and cross blue line
    def stage_one():
        while True:
            avoidWhite()
            tango.setTarget(MOTORS, 5400)

            #Find PINK line
            img = getFrame(1)
            x, y = findCoG(img)
            if y > 400:
                time.sleep(1)
                tango.setTarget(MOTORS, 6000)
                client.client.sendData("Crossed the Line")
                rawCapture.truncate(0)
                break
            
            rawCapture.truncate(0)
            key = cv2.waitKey(1) & 0xFF
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                shutdown()
                break

#Grab ice
def stage_two():
    #set some stuff like tilt
    while True:
        img = getFrame(-1)
        #showFrame(img)
        face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(img, 1.3, 4)
        if(len(faces) != 0):
                if(findHumanFlag):
                        client.client.sendData("Oh, Hello")
                        findHumanFlag = False
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
                                temp = (19000-w*h) / 5600
                                motors = 5400
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
                            client.client.sendData("Give me ice prease")
                            rawCapture.truncate(0)
                            break

        rawCapture.truncate(0)
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            shutdown()
            break

    #Grab ice with arm
    init_flag = True
    while True:
        #maybe look right/down a bit
        img = getFrame(3)
        if(init_flag):
            tango.setTarget(SHOULDER, 7000)
        x, y = findCoG(img)
        if x != -1 and y != -1:
            time.sleep(1.5)
            tango.setTarget(HAND, 10000)
            tango.setTarget(SHOULDER, 6000)
            break
        
        '''
        shoulder = 6500
        hand = 4000
        headTitlt = 4000
        headTurn = 4000
        tango.setTarget(SHOULDER, shoulder)
        tango.setTarget(HAND, hand)
        tango.setTarget(HEADTILT, headTilt)
        tango.setTarget(HEADTURN, headTurn)
        findIce()
        hand = 6000
        headTurn = 6000
        tango.setTarget(HAND, hand)
        tango.setTarget(HEADTURN, headTurn)


        '''
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            shutdown()
            break

#Find and cross pink line
def stage_three():
    headTilt = 4500
    headTilt = 4000
    tango.setTarget(HEADTILT, headTilt)
    tango.setTarget(TURN, 7000)
    flag = False

    while True:
        img = getFrame(1)
        showFrame(img)
        x, y = findCoG(img)

        if 300 <= x <= 380:
            print("Forward ini")
            #go forward toward the line
            tango.setTarget(TURN, 6000)
            tango.setTarget(MOTORS, 5200)
            flag = True

        if y > 400 and flag:
            time.sleep(.8)
            tango.setTarget(MOTORS, 6000)
            client.client.sendData("Crossed the Line")
            rawCapture.truncate(0)
            break

        rawCapture.truncate(0)
        if threshold() and flag:
            if avoidWhite():
                break

        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
                shutdown()
                break


#Navigate through minefield
def stage_four():
        while True:
            avoidWhite()
            tango.setTarget(MOTORS, 5400)

            #Find yellow line
            img = getFrame(0)
            x, y = findCoG(img)

            if y > 400:
                time.sleep(.8)
                tango.setTarget(MOTORS, 6000)
                client.client.sendData("Crossed the Line")
                rawCapture.truncate(0)
                break
            
            rawCapture.truncate(0)
            key = cv2.waitKey(1) & 0xFF
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                shutdown()
                break

#drop ice in bin
def final_stage():
    headTilt = 4000
    tango.setTarget(HEADTILT, headTilt)
    tango.setTarget(TURN, 7000)
    flag = False
    size = 0

    while True:
        img = getFrame(3)
        showFrame(3)
        x, y = findCoG(img)

        if 300 <= x <= 380:
            print("Found bin")
            client.client.sendData("Found the Bin")
            #go forward toward the bin
            tango.setTarget(TURN, 6000)
            tango.setTarget(MOTORS, 5200)
            flag = True

        #Uses area and center of gravity to compute proper orientation
        if flag:
            ret,thresh = cv2.threshold(gray,127,255,1)
            contours,h = cv2.findContours(thresh,1,2)
            for contour in contours:
                sides = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
                if sides == 4:
                    area = cv2.countourArea(contour)
                    if area > size:
                        size = area
            if area > 8000:
                if x > 320:
                    orientate(False)
                elif x < 320:
                    orientate(True)
                time.sleep(.5)
                tango.setTarget(MOTORS, 6000)
            rawCapture.truncate(0)
            break


        rawCapture.truncate(0)
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop 
        if key == ord("q"):
            shutdown()
            break

    #Dropping ice in Bin
    tango.setTarget(SHOULDER, 7000)
    tango.setTarget(BODY, 6600)
    client.client.sendData("Dropping. And Done.")
    tango.setTarget(HAND, 6000)


def main():
    print("Init stage")
    init_stage()

    print("Stage 1")
    stage_one()

    print("Stage 2")
    stage_two()

    print("Obtaining Ice")
    get_ice()

    print("Stage 3")
    stage_three()

    print("Stage 4")
    stage_four()

    print("Final Stage")
    final_stage()

    shutdown()

main()
def test():
    shoulder = 8000
    hand = 6000
    headTitlt = 4000
    headTurn = 4000
    tango.setTarget(SHOULDER, shoulder)
    tango.setTarget(HAND, hand)
    tango.setTarget(HEADTILT, headTilt)
    tango.setTarget(HEADTURN, headTurn)
    findIce()
    hand = 10000
    headTurn = 6000
    tango.setTarget(HAND, hand)
    tango.setTarget(HEADTURN, headTurn)

#test()