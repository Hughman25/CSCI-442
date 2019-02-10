import numpy as np

import cv2

'''
print(cv2.__version__)
for i in dir(cv2):
    if i.startswith('COLOR_'):
        print(i)
'''

'''
image = cv2.imread("clouds.jpg")
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Over the Clouds", image)
cv2.imshow("Over the Clouds - gray", gray_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''


def main():
    """
    high level support for doing this and that.
    """     
    '''
    IMG = np.zeros((512, 512, 1), np.uint8)
    WIDTH, HEIGHT, CHANNEL = IMG.shape
    IMG2 = 100* np.ones((WIDTH, HEIGHT, 1), np.uint8)
    IMG3 = 100* np.ones((WIDTH, HEIGHT, 1), np.uint8)
    IMG4 = cv2.add(IMG2, IMG3)
    cv2.imshow("image 4:", IMG4)
    '''
    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)
    
    if vc.isOpened(): # try to get the first frame
        # Convert BGR to HSV
        rval, frame = vc.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # define range of blue color in HSV
        lower_blue = np.array([110,50,50])
        upper_blue = np.array([130,255,255])

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_green, upper_green)
    else:
        rval = False

    while rval:
        cv2.imshow("preview", frame)
        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            break
    cv2.destroyWindow("preview")

main()