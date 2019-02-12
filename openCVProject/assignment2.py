import numpy as np
import cv2

def nothing(x):
    pass

def onMouse(event, x, y, flag, param):
        if(event == cv2.EVENT_LBUTTONDOWN):
                print x, " ", y
                return 1
        else:
                return 0

def main():
    original = cv2.namedWindow("Original", cv2.WINDOW_KEEPRATIO)
    hsv = cv2.namedWindow("HSV", cv2.WINDOW_KEEPRATIO)

    mask = cv2.namedWindow("Mask", cv2.WINDOW_KEEPRATIO)
    #res = cv2.namedWindow("Res", cv2.WINDOW_KEEPRATIO)

    vc = cv2.VideoCapture(0)
    cv2.moveWindow("Original", 0, 0)
    cv2.moveWindow("HSV", 300, 0)
    cv2.moveWindow("Mask",700, 0)
   # cv2.moveWindow("Res", 1100, 0)
    # create trackbars for color change
    cv2.createTrackbar('RL', 'HSV', 10, 255, nothing)
    cv2.createTrackbar('RU', 'HSV', 10, 255, nothing)
    cv2.createTrackbar('GL', 'HSV', 10, 255, nothing)
    cv2.createTrackbar('GU', 'HSV', 10, 255, nothing)
    cv2.createTrackbar('BL', 'HSV', 10, 255, nothing)
    cv2.createTrackbar('BU', 'HSV', 10, 255, nothing)

    # create switch for ON/OFF functionality
    #switch = '0 : OFF \n1 : ON'
    #cv2.createTrackbar(switch, 'Original',0,1,nothing)
    

    if vc.isOpened(): # try to get the first frame
        # Convert BGR to HSV
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #set mouse callback to print out color values
        cv2.setMouseCallback("Original", onMouse)
        if(onMouse == 1):
                cv2.rectangle("Original", 240, 340, (0, 255, 0), 3, 8)
        # get current positions of four trackbars
        rl = cv2.getTrackbarPos('RL','HSV')
        gl = cv2.getTrackbarPos('GL','HSV')
        bl = cv2.getTrackbarPos('BL','HSV')
        ru = cv2.getTrackbarPos('RU','HSV')
        gu = cv2.getTrackbarPos('GU','HSV')
        bu = cv2.getTrackbarPos('BU','HSV')
        #s = cv2.getTrackbarPos(switch,'HSV')
        
        # define range of blue color in HSV
        lower_red = np.array([rl, gl, bl])
        upper_red = np.array([ru, gu, bu])
        lower_blue = np.array([rl, gl, bl])
        upper_blue = np.array([ru, gu, bu])
        lower_green = np.array([rl, gl, bl])
        upper_green = np.array([ru, gu, bu])
        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_green, upper_green)

        # Bitwise-AND mask and original image
        #res = cv2.bitwise_and(frame, frame, mask=mask)
        
        cv2.imshow("Original", frame)
        cv2.imshow("HSV", hsv)
        cv2.imshow("Mask", mask)
        #cv2.imshow("Res", res)


        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            break
    cv2.destroyAllWindows()

main()
