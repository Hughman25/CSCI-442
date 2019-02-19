'''
Authors: Matthew Sagen and Hugh Jackovich
'''

import cv2
import numpy as np




def updateText(pic, red, green, blue):
    red = "Red:" + str(red)
    green = "Green:" + str(green)
    blue = "Blue:" + str(blue)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(pic, red, (10, 50), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(pic, green, (10, 75), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(pic, blue, (10, 100), font, 1, (0, 0, 0), 1, cv2.LINE_AA)

def main():

    picture_1 = cv2.imread("candy1.jpg", cv2.IMREAD_COLOR)
    picture_2 = cv2.imread('candy2.jpg', cv2.IMREAD_COLOR)
    cv2.namedWindow("Candy", cv2.WINDOW_KEEPRATIO)
    cv2.namedWindow("Candy2", cv2.WINDOW_KEEPRATIO)
    cv2.moveWindow("Candy", 0, 0)
    cv2.moveWindow("Candy2", 600, 0)
    red = 0
    green = 0
    blue = 0
    #initialize counts to 0
    updateText(picture_1, red, green, blue)
    updateText(picture_2, red, green, blue)


    cv2.imshow("Candy", picture_1)
    cv2.imshow("Candy2", picture_2)



    cv2.waitKey(0)
    cv2.destroyAllWindows()





main()