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
    #read the original images into memory
    picture_1 = cv2.imread("imagesWOvideo/one.jpg", cv2.IMREAD_COLOR)
    picture_2 = cv2.imread("imagesWOvideo/two.jpg", cv2.IMREAD_COLOR)
    picture_3 = cv2.imread("imagesWOvideo/three.jpg", cv2.IMREAD_COLOR)
    picture_4 = cv2.imread("imagesWOvideo/four.jpg", cv2.IMREAD_COLOR)
    #blur the images with 5x5
    blur1 = cv2.blur(picture_1, (5, 5))
    blur2 = cv2.blur(picture_2, (5, 5))
    blur3 = cv2.blur(picture_3, (5, 5))
    blur4 = cv2.blur(picture_4, (5, 5))
    #run canny edge detector to detect edges
    edge1 = cv2.Canny(blur1, 50, 150)
    edge2 = cv2.Canny(blur2, 50, 150)
    edge3 = cv2.Canny(blur3, 50, 150)
    edge4 = cv2.Canny(blur4, 50, 150)
    #create named windows
    cv2.namedWindow("Candy1", cv2.WINDOW_KEEPRATIO)
    cv2.namedWindow("Candy2", cv2.WINDOW_KEEPRATIO)
    cv2.namedWindow("Candy3", cv2.WINDOW_KEEPRATIO)
    cv2.namedWindow("Candy4", cv2.WINDOW_KEEPRATIO)
    cv2.namedWindow("Edge1", cv2.WINDOW_KEEPRATIO)
    cv2.namedWindow("Edge2", cv2.WINDOW_KEEPRATIO)
    cv2.namedWindow("Edge3", cv2.WINDOW_KEEPRATIO)
    cv2.namedWindow("Edge4", cv2.WINDOW_KEEPRATIO)
    #move named windows 
    cv2.moveWindow("Candy1", 0, 0)
    cv2.moveWindow("Candy2", 410, 0)
    cv2.moveWindow("Candy3", 820, 0)
    cv2.moveWindow("Candy4", 0, 350)
    cv2.moveWindow("Edge1", 410, 350)
    cv2.moveWindow("Edge2", 820, 350)
    cv2.moveWindow("Edge3", 900, 350)
    cv2.moveWindow("Edge4", 0, 350)
    #initialize r,g,b,y,o,br values
    red = 0
    green = 0
    blue = 0
    yellow = 0
    orange = 0
    brown = 0
    #initialize counts to 0 and display on image
    updateText(picture_1, red, green, blue, yellow, orange, brown)
    updateText(picture_2, red, green, blue, yellow, orange, brown)
    updateText(picture_3, red, green, blue, yellow, orange, brown)
    updateText(picture_4, red, green, blue, yellow, orange, brown)

    #get hsv values for images
    hsv1 = cv2.cvtColor(picture_1, cv2.COLOR_BGR2HSV) 
    hsv2 = cv2.cvtColor(picture_2, cv2.COLOR_BGR2HSV)
    hsv3 = cv2.cvtColor(picture_2, cv2.COLOR_BGR2HSV)
    hsv4 = cv2.cvtColor(picture_2, cv2.COLOR_BGR2HSV)

    lower_red = np.array([150, 0, 16]) #red
    upper_red = np.array([197, 38, 56])

    lower_blue = np.array([27, 139, 195]) #blue
    upper_blue = np.array([77, 189, 245])

    lower_green = np.array([29, 152, 65]) #green
    upper_green = np.array([69, 192, 105])

    lower_yel = np.array([235, 235, 100]) #yellow
    upper_yel = np.array([255, 255, 200])

    lower_or = np.array([222, 91, 14]) #orange
    upper_or = np.array([262, 131, 54])

    lower_br = np.array([76, 38, 32]) #brown
    upper_br = np.array([116, 78, 72])

    '''
    todo: draw a circle object around a color if its whithin our threshold. Increment number of circle objects with same 
    color value. 
    '''
    '''
    maybe a method to mask for each color, and draw circles around each color...
    '''
    # Threshold the HSV image to get only specified colors
    mask = cv2.inRange(hsv1, lower_br, upper_br) #yellow somehow
    

    #cv2.imshow("Mask", mask)
    cv2.imshow("Candy1", picture_1)
    cv2.imshow("Candy2", picture_2)
    cv2.imshow("Candy3", picture_3)
    cv2.imshow("Candy4", picture_4)
    cv2.imshow("Edge1", edge1)
    cv2.imshow("Edge2", edge2)
    cv2.imshow("Edge3", edge3)
    cv2.imshow("Edge4", edge4)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

main()