import numpy as np
import cv2

def nothing(x):
    pass

def main():
    original = cv2.namedWindow("Original", cv2.WINDOW_KEEPRATIO)
    mask = cv2.namedWindow("Mask", cv2.WINDOW_KEEPRATIO)
    res = cv2.namedWindow("Res", cv2.WINDOW_KEEPRATIO)

    vc = cv2.VideoCapture(0)
    cv2.moveWindow("Original", 30, 30)
    # create trackbars for color change
    cv2.createTrackbar('RL', 'Original', 0, 255, nothing)
    cv2.createTrackbar('GL', 'Original', 0, 255, nothing)
    cv2.createTrackbar('BL', 'Original', 0, 255, nothing)
    cv2.createTrackbar('RU', 'Original', 0, 255, nothing)
    cv2.createTrackbar('GU', 'Original', 0, 255, nothing)
    cv2.createTrackbar('BU', 'Original', 0, 255, nothing)


    # create switch for ON/OFF functionality
    switch = '0 : OFF \n1 : ON'
    cv2.createTrackbar(switch, 'Original',0,1,nothing)

    if vc.isOpened(): # try to get the first frame
        # Convert BGR to HSV
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # get current positions of four trackbars
        rl = cv2.getTrackbarPos('RL','Original')
        gl = cv2.getTrackbarPos('GL','Original')
        bl = cv2.getTrackbarPos('BL','Original')
        ru = cv2.getTrackbarPos('RU','Original')
        gu = cv2.getTrackbarPos('GU','Original')
        bu = cv2.getTrackbarPos('BU','Original')
        s = cv2.getTrackbarPos(switch,'Original')
        
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
        res = cv2.bitwise_and(frame,frame, mask= mask)
        
        cv2.imshow("Original", frame)
        cv2.imshow('Mask', mask)
        cv2.imshow('Res', res)

        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            break
    cv2.destroyWindow("Original")

main()
