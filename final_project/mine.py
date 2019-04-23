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
ELBOW = 8

#Set default motor values
tango = maestro.Controller()
body = 5700
headTurn = 6000
headTilt = 6000
turn = 6000
maxMotor = 5675
maxLeftTurn = 7000
maxRightTurn = 5000
motors = 6000
shoulder = 6000
hand = 6000
elbow = 6000

#Assign initial values to motors
tango.setTarget(HEADTURN, headTurn)
tango.setTarget(HEADTILT, headTilt)
tango.setTarget(TURN, turn)
tango.setTarget(BODY, body)
tango.setTarget(SHOULDER, shoulder)
tango.setTarget(HAND, hand)
tango.setTarget(ELBOW, elbow)
#set arm targets

#global flags/vars
bodyFlag = True
turnFlag = -1
i = 0

#values for finding orange line with hsv
lower_yellow_bound = np.array([20, 50, 50], dtype="uint8")
upper_yellow_bound = np.array([39, 255, 255], dtype="uint8")
lower_pink_bound = np.array([125, 35, 100], dtype="uint8")
upper_pink_bound = np.array([180, 125, 125], dtype="uint8")
lower_white_bound = np.array([0, 0, 240], dtype="uint8")
upper_white_bound = np.array([255, 15, 255], dtype="uint8")
lower_green_bound = np.array([45, 50, 50], dtype="uint8")
upper_green_bound = np.array([75, 255, 255], dtype="uint8")


time.sleep(2)

#Returns the desired image for a given stage
def getFrame(stage):
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        #image = cv2.fastNlMeansDenoisingColored(image,None,10,10,7,21) #change 21 lower to increase performance, should be odd
                                                                        #change 1st 10 change strength of noise removal, may add after blur.
        if stage != -1:
            blur = cv2.GaussianBlur(image, (5, 5), 1)
            #image = cv2.fastNlMeansDenoisingColored(image,None,10,10,7,21)
            hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
            #image = cv2.Canny(mask, 100, 50) #For safe keeping
        if stage == 0:
            mask = cv2.inRange(hsv, lower_yellow_bound, upper_yellow_bound)
        elif stage == 1:
            mask = cv2.inRange(hsv, lower_pink_bound, upper_pink_bound)
        elif stage == 2:
            mask = cv2.inRange(hsv, lower_white_bound, upper_white_bound)
        elif stage == 3:
            mask = cv2.inRange(hsv, lower_green_bound, upper_green_bound)
        break
    return image


#Shows the frame
def showFrame(image, flag):
    cv2.imshow("Main Camera", image)
    
    #Apparently fixed an issue with a frozen frame not being replaced by new one.
    if flag:
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            shutdown()


#Stops all motors but not program, had an issue with stopping a motor, this worked.
def stop():
    motors = 6000
    turn = 6000
    headTilt = 6000
    tango.setTarget(MOTORS, motors)
    tango.setTarget(TURN, turn)
    tango.setTarget(HEADTILT, headTilt)
    tango.setTarget(BODY, 6000)
    tango.setTarget(HAND, 6000)
    tango.setTarget(SHOULDER, 6000)
    rawCapture.truncate(0)


#Shuts down all motors to their original origin and ends program
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
    rawCapture.truncate(0)
    quit()


#Search positions for finding a human, rotates accordingly
def nextSearchPosition():
        positions = [(6000, 6000, 6000), (6000, 7000, 6500), (6800, 7000, 6500), (6000, 7000, 6500), (5200, 7000, 6500), (6000, 6000, 6000),
                        (5200, 5000, 5500), (6000, 5000, 5500), (6800, 5000, 5500)] #tilt, turn, bodyturn
        global headTilt, headTurn, i
        headTilt = positions[i%9][0]
        headTurn = positions[i%9][1]
        tango.setTarget(HEADTURN, headTurn)
        tango.setTarget(HEADTILT, headTilt)
        tango.setTarget(BODY, positions[i%9][2])
        time.sleep(1.5)
        i += 1


#Centers the body of the robot towards a square object
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
        

#Centers the screen on a square object
def centerScreen(xabs, yabs, xdist, ydist):
    if((xabs > 60) or (yabs > 50)):
        xdist = xdist + int(xdist*.3)
        ydist = ydist + int(ydist*.3)
        tango.setTarget(HEADTURN, 6000 + (xdist*2))
        tango.setTarget(HEADTILT, 6000 + (int(ydist*2.5)))
    elif((xabs < 60) and (yabs > 50)):
        return True
    return False


#Orientates the robot if it is not properly positioned for the bin
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


#Finds the highest white pixel y value.
def findHighestY(img):
   white_pixels = np.argwhere(img >= 254)
   highest_y = 0
   for y, x in white_pixels:
       if y > highest_y:
           highest_y = y
   return highest_y


#Method for avoiding white objects
def avoidWhite():
    global turnFlag
    img = getFrame(2)
    showFrame(img, False)
    high_y = findHighestY(img)
    x, y = findCoG(img, True)
    size = len(np.argwhere(img >= 254))

    if high_y >= 410 and 380 > x > 260:
        print("backwards")
        if turnFlag == 3:
            tango.setTarget(TURN, 5200)
            time.sleep(.85)
            tango.setTarget(TURN, 6000)
            turnFlag == 4
            return 1
        #tango.setTarget(MOTORS, 6000)
        #time.sleep(0.1)
        tango.setTarget(MOTORS, 6800)
        time.sleep(0.4)
        tango.setTarget(MOTORS, 6000)
        turnFlag == 3

    if 315 > x > 200:
        turnFlag = 1
        print("right turn")
        tango.setTarget(TURN, 5200)
        time.sleep(.85)
        tango.setTarget(TURN, 6000)
    elif 470 > x > 325:
        turnFlag = 0
        print("left turn")
        tango.setTarget(TURN, 6800)
        time.sleep(.85)
        tango.setTarget(TURN, 6000)

    if size < 100000:
        if turnFlag == 1:
            tango.setTarget(TURN, 6800)
            time.sleep(.85)
            tango.setTarget(TURN, 6000)
            turnFlag = -1
            rawCapture.truncate(0)
            return 1
        elif turnFlag == 0:
            tango.setTarget(TURN, 5200)
            time.sleep(.85)
            tango.setTarget(TURN, 6000)
            rawCapture.truncate(0)
            return 1
    rawCapture.truncate(0)
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        shutdown()
        return 1


#function to determine center of gravity of white objects
def findCoG(img, flag):
    white_pixels = np.argwhere(img >= 254)
    size = len(white_pixels)
    sumX = 0
    sumY = 0
    if size < 125:
        return -1, -1
    for y, x in white_pixels:
        if flag:
            if y > 125:
                sumX += x
                sumY += y
        else:
            sumX += x
            sumY += y

    if(size > 0):
        sumX = sumX / size
        sumY = sumY / size
    else:
        return -1, -1
    return sumX, sumY


#Finds white pixels near the center of the image, returns if found 150
def findCenterWhitePixels(img):
    white_pixels = np.argwhere(img >= 254)
    count = 0
    for y, x in white_pixels:
        if y > 180:
            if 350 > x > 290:
                count += 1
    if count > 150:
        return 1
    else:
        return 0


#Method to ignore noise while turning
def threshold():
    img = getFrame(2)
    white_pixels = np.argwhere(img >= 254)
    size = len(white_pixels)
    rawCapture.truncate(0)

    if size < 100000:
        if findCenterWhitePixels(img):
            return 1
        return 0
    else:
        return 1


#Find yellow line and cross it
def init_stage():
    headTilt = 4000
    tango.setTarget(HEADTILT, headTilt)
    tango.setTarget(TURN, 7000)
    flag = False

    while True:
        if not flag:
            tango.setTarget(TURN, 7000)
        img = getFrame(0)
        showFrame(img, False)
        y = findHighestY(img)
        x, yx = findCoG(img, True)
        
        #can shorten this dist and make it turn if outside
        '''
        if 300 <= x <= 340:
            print("Forward ini")
            #go forward toward the line
            if not flag:
                tango.setTarget(TURN, 6000)
                tango.setTarget(TURN, 5100)
                time.sleep(0.35)
            
            tango.setTarget(TURN, 6000)
            tango.setTarget(MOTORS, 5200)
            flag = True
        elif x < 300:
            tango.setTarget(TURN, 5200)
            time.sleep(1)
            tango.setTarget(TURN, 6000)
        elif x > 340:
            tango.setTarget(TURN, 6800)
            time.sleep(1)
            tango.setTarget(TURN, 6000)
        else:
            flag  = False
        '''
        if 260 <= x <= 420:
            print("Forward ini")
            #go forward toward the line
            if not flag:
                tango.setTarget(TURN, 6000)
                tango.setTarget(TURN, 5100)
                time.sleep(0.35)
            
            tango.setTarget(TURN, 6000)
            tango.setTarget(MOTORS, 5200)
            flag = True
        else:
            flag  = False
   
        if y > 420 and flag:
            time.sleep(.8)
            tango.setTarget(MOTORS, 6000)
            client.client.sendData("Rocky area ahead")
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


#Avoid rocks, find and cross pink line
def stage_one():
    flag = False
    while True:
        avoidWhite()
        
        tango.setTarget(MOTORS, 5200)

        #Find PINK line
        img = getFrame(1)
        y = findHighestY(img)
        x, yx = findCoG(img, True)
        if y > 420 and flag:
            time.sleep(2)
            tango.setTarget(MOTORS, 6000)
            client.client.sendData("Mining area reached")
            rawCapture.truncate(0) 
            break
        
        rawCapture.truncate(0)
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            shutdown()
            break
        flag = True

#Find human and grab ice
def stage_two():
    findHumanFlag = True
    distFlag = True
    tango.setTarget(HEADTILT, 6300)

    while True:
        if findHumanFlag:
            nextSearchPosition()
        img = getFrame(-1)
        showFrame(img, True)
        face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(img, 1.3, 4)
        if(len(faces) != 0):
                if(findHumanFlag):
                        client.client.sendData("Oh, Hello")
                        findHumanFlag = False
                x,y,w,h = faces[0]
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
                            break

        rawCapture.truncate(0)
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            shutdown()
            break
    rawCapture.truncate(0)
    #Grab ice with arm
    init_flag = True
    while True:
        #maybe look right/down a bit
        img = getFrame(3)
        showFrame(img, False)
        if(init_flag):
            tango.setTarget(ELBOW, 7000)
            tango.setTarget(SHOULDER, 7000)
        x, y = findCoG(img, True)
        if x != -1 and y != -1:
            time.sleep(1.8)
            tango.setTarget(HAND, 10000)
            rawCapture.truncate(0)
            break
        
        rawCapture.truncate(0)
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            shutdown()
            break

#Find and cross pink line again
def stage_three():
    headTilt = 4000
    tango.setTarget(HEADTILT, headTilt)
    tango.setTarget(TURN, 7000)
    time.sleep(1)
    flag = False

    while True:
        if not flag:
            tango.setTarget(TURN, 7000)
        img = getFrame(1)
        showFrame(img, False)
        y = findHighestY(img)
        x, yx = findCoG(img, True)

        if 280 <= x <= 380:
            print("Forward ini")
            #go forward toward the line
            tango.setTarget(TURN, 6000)
            tango.setTarget(MOTORS, 5200)
            flag = True
        else:
            flag = False

        if y > 420 and flag:
            time.sleep(.8)
            tango.setTarget(MOTORS, 6000)
            client.client.sendData("Rocky area ahead")
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


#Find and cross yellow line again
def stage_four():
        while True:
            avoidWhite()
            tango.setTarget(MOTORS, 5200)

            #Find yellow line
            img = getFrame(0)
            y = findHighestY(img)
            x, yx = findCoG(img, True)

            if y > 400:
                time.sleep(.8)
                tango.setTarget(MOTORS, 6000)
                client.client.sendData("Starting area reached   ")
                rawCapture.truncate(0)
                break
            
            rawCapture.truncate(0)
            key = cv2.waitKey(1) & 0xFF
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                shutdown()
                break

#Find bin and drop the ice in it
def final_stage():
    headTilt = 5000
    tango.setTarget(HEADTILT, headTilt)
    flag = False
    orientate_flag = -1
    right_hand_side = False

    while True:
        if not flag:
            tango.setTarget(TURN, 7000)
        img = getFrame(3)
        showFrame(img, False)
        x, y = findCoG(img, False)
        if x == -1 and y == -1:
            flag = False
        # if x < 320: #turn left
        #     orientate_flag = 1
        # elif x > 320: #turn right
        #     orientate_flag = 0


        if 290 <= x <= 350:
            if not flag:
                client.client.sendData("Found the Bin")
            #go forward toward the bin
            tango.setTarget(TURN, 6000)
            tango.setTarget(MOTORS, 5200)
            flag = True
        elif x < 300:
            tango.setTarget(TURN, 5200)
            time.sleep(1)
            tango.setTarget(TURN, 6000)
        elif x > 380:
            tango.setTarget(TURN, 6800)
            time.sleep(1)
            tango.setTarget(TURN, 6000)
            right_hand_side = True
        else:
            flag = False

        #Uses area and center of gravity to compute proper orientation
        if flag:
            if x == -1 and y == -1:
                # if orientate_flag:
                #     orientate(False)
                # elif not orientate_flag:
                #     orientate(True)
                time.sleep(.5)
                stop()
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
    if right_hand_side:
        tango.setTarget(BODY, 9500)
    else:
        tango.setTarget(BODY, 8000)
    time.sleep(.8)
    client.client.sendData("Dropping. And Done.Goodbye")
    tango.setTarget(HAND, 6000)


#Main method for calling stages in order, though, sometimes its nice to go back.
def main():
    #shutdown()
    print("Init stage")
    init_stage()

    print("Stage 1")
    stage_one()

    print("Stage 2")
    stage_two()

    print("Obtaining Ice")


    print("Stage 3")
    stage_three()

    print("Stage 4")
    stage_four()

    print("Final Stage")
    final_stage()
  
    shutdown()

main()


#tester method
def test():
    while True:
        img = getFrame(3)
        showFrame(img)
        
        rawCapture.truncate(0)
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop 
        if key == ord("q"):
            shutdown()
            break

# test()
# final_stage()
# shutdown()