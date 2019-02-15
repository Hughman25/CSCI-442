import cv2
import numpy as np

#primary windows
cap = cv2.VideoCapture(0)
cv2.namedWindow("Original", cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("HSV", cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("Black/White", cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("Erosion", cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("Dilation", cv2.WINDOW_KEEPRATIO)

cv2.moveWindow("Original", 0, 0)
cv2.moveWindow("HSV", 400, 0)
cv2.moveWindow("Black/White", 800, 0)
cv2.moveWindow("Erosion", 400, 400)
cv2.moveWindow("Dilation", 800, 400)

#initialize variables so we can use 'em
hsv = 0
minHSV = np.array([0, 0, 0])
maxHSV = np.array([0, 0, 0])
res = [0, 0, 0]
kernel = np.ones((5,5), np.uint8)

def nothing(x):
    pass

#set new pixel to track when clicked (only for HSV window)
def mouseCall(evt, x, y, flags, pic):
    if evt==cv2.EVENT_LBUTTONDOWN:
        global res
        res = hsv[y][x]
        print(str(x) + ", " + str(y))
        print(res)

#set scalar values for tracking every loop
def setScalars(h, s, v):
    global res, minHSV, maxHSV
    minHSV = np.array([res[0] - h, res[1] - s, res[2] - v])
    maxHSV = np.array([res[0] + h, res[1] + s, res[2] + v])

#create sliders
cv2.createTrackbar("Hue Tol.", "HSV", 0, 255,nothing)
cv2.createTrackbar("Sat Tol.", "HSV", 0, 255,nothing)
cv2.createTrackbar("Val Tol.", "HSV", 0, 255,nothing)
cv2.setMouseCallback("HSV", mouseCall, hsv)

rval, frame = cap.read() #read in video
blank1 = np.float32(frame)
blank2 = np.float32(frame)
img = np.float32(frame)
absDiff = np.float32(frame)

while True:

    val, img = cap.read() #read in video
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #convert to HSV
    black_white = cv2.inRange(hsv, minHSV, maxHSV)    #black and white image to track stuff
    img_erosion = cv2.erode(black_white, kernel, iterations=2)    #erode white
    img_dilation = cv2.dilate(img_erosion, kernel, iterations=2) #dilate black

    blur = cv2.GaussianBlur(img,(5,5),0)
    cv2.accumulateWeighted(blur, blank1, .320)
    res1 = cv2.convertScaleAbs(blank1)
    absDiff = cv2.absdiff(img, res1)
    grayimg = cv2.cvtColor(absDiff, cv2.COLOR_BGR2GRAY)
    _, grayimg = cv2.threshold(grayimg, 25, 255, cv2.THRESH_BINARY)
    grayimg = cv2.GaussianBlur(grayimg,(5,5),0)
    _, grayimg = cv2.threshold(grayimg, 220, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(grayimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(frame, contours, -1, (0,255,0), 3)
    cv2.imshow("Video", frame)
    cv2.imshow("Abs Diff", grayimg)


    #create images in windows
    cv2.imshow("Original", img)
    cv2.imshow("HSV", hsv)
    cv2.imshow("Black/White", black_white)
    cv2.imshow('Erosion', img_erosion)
    cv2.imshow('Dilation', img_dilation)
    k = cv2.waitKey(1)
    if k == 27:
        break

    #get current positions of three trackbars
    h = cv2.getTrackbarPos('Hue Tol.', 'HSV')
    s = cv2.getTrackbarPos('Sat Tol.', 'HSV')
    v = cv2.getTrackbarPos('Val Tol.', 'HSV')

    #update tracking scalars
    setScalars(h, s, v)

cv2.destroyAllWindows()
