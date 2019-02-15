import numpy as np
import cv2

x_loc = None
y_loc = None

def nothing(x):
    pass

def onMouse(event, x, y, flag, param):
        if(event == cv2.EVENT_LBUTTONDOWN):
                x_loc = x
                y_loc = y
                print x_loc, " ", y_loc
        else:
            pass
def main():
    original = cv2.namedWindow("Original", cv2.WINDOW_KEEPRATIO)
    hsv = cv2.namedWindow("HSV", cv2.WINDOW_KEEPRATIO)
    mask = cv2.namedWindow("Mask", cv2.WINDOW_KEEPRATIO)
    res1 = cv2.namedWindow("Avg1", cv2.WINDOW_KEEPRATIO)
    res2 = cv2.namedWindow("Avg2", cv2.WINDOW_KEEPRATIO)

    #res = cv2.namedWindow("Res", cv2.WINDOW_KEEPRATIO)

    vc = cv2.VideoCapture(0)
    cv2.moveWindow("Original", 0, 0)
    cv2.moveWindow("HSV", 300, 0)
    cv2.moveWindow("Mask",700, 0)
    cv2.moveWindow("Avg1",300, 300)

    cv2.moveWindow("Avg2",700, 300)

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
        rval, frame = vc.read()
    else:
        rval = False

    avg1 = np.float32(frame)
    avg2 = np.float32(frame)
    while rval:
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h = hsv[0]
        s = hsv[1]
        v = hsv[2]
        print "H:", h, " S: ", s, "V: ", v
        cv2.accumulateWeighted(frame,avg1,0.1)
        cv2.accumulateWeighted(frame,avg2,0.01)
        res1 = cv2.convertScaleAbs(avg1)
        res2 = cv2.convertScaleAbs(avg2)

        cv2.FindContours("Original", )
        #set mouse callback to print out color values
        cv2.setMouseCallback("Original", onMouse)
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
        cv2.imshow("Avg1", res1)
        cv2.imshow('Avg2',res2)
        #cv2.imshow("Res", res)


        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            break
    cv2.destroyAllWindows()

main()
