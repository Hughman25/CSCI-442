'''
Authors: Matthew Sagen and Hugh Jackovich
'''

import cv2
import numpy as np



#helper method to update text in windows.
def updateText(pic, red, green, blue, yellow, orange, brown):
    red = "Red:" + str(red)
    green = "Green:" + str(green)
    blue = "Blue:" + str(blue)
    yellow = "Yellow:" + str(yellow)
    orange = "Orange:" + str(orange)
    brown = "Brown:" + str(brown)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(pic, red, (10, 50), font, 1, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(pic, green, (10, 75), font, 1, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(pic, blue, (10, 100), font, 1, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(pic, yellow, (10, 125), font, 1, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(pic, orange, (10, 150), font, 1, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(pic, brown, (10, 175), font, 1, (0, 0, 0), 2, cv2.LINE_AA)

def main():

    picture_1 = cv2.imread("imagesWOvideo/one.jpg", cv2.IMREAD_COLOR)
    picture_2 = cv2.imread("imagesWOvideo/two.jpg", cv2.IMREAD_COLOR)
    picture_3 = cv2.imread("imagesWOvideo/three.jpg", cv2.IMREAD_COLOR)
    picture_4 = cv2.imread("imagesWOvideo/four.jpg", cv2.IMREAD_COLOR)

    cv2.namedWindow("Candy1", cv2.WINDOW_KEEPRATIO)
    cv2.namedWindow("Candy2", cv2.WINDOW_KEEPRATIO)
    cv2.namedWindow("Candy3", cv2.WINDOW_KEEPRATIO)
    cv2.namedWindow("Candy4", cv2.WINDOW_KEEPRATIO)
    cv2.moveWindow("Candy1", 0, 0)
    cv2.moveWindow("Candy2", 410, 0)
    cv2.moveWindow("Candy3", 820, 0)
    cv2.moveWindow("Candy4", 0, 350)
    red = 0
    green = 0
    blue = 0
    yellow = 0
    orange = 0
    brown = 0
    #initialize counts to 0
    updateText(picture_1, red, green, blue, yellow, orange, brown)
    updateText(picture_2, red, green, blue, yellow, orange, brown)
    updateText(picture_3, red, green, blue, yellow, orange, brown)
    updateText(picture_4, red, green, blue, yellow, orange, brown)

    #todo: find different colors in the image, determine if they are circles?


    cv2.imshow("Candy1", picture_1)
    cv2.imshow("Candy2", picture_2)
    cv2.imshow("Candy3", picture_2)
    cv2.imshow("Candy4", picture_2)



    cv2.waitKey(0)
    cv2.destroyAllWindows()





main()