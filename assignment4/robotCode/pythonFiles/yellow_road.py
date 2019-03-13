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

# allow the camera to warmup
time.sleep(0.1)
def findCoG(img):
    white_pixels = np.argwhere(img >= 200)
    size = white_pixels.size
    sumX = 0
    sumY
    for(x, y in white_pixels):
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
    pic = cv2.Canny(image, 100, 170)

    cog = findCoG(pic)
    cv2.Rectangle(pic, (x+10, y+10), (x-10, y-10), (0, 0, 255))
    # show the frame
    cv2.imshow("Frame", pic)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
            break



