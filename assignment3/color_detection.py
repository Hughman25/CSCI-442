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
    pictures = [picture_1, picture_2, picture_3, picture_4]
    #blur the images with 5x5
    blurs = []
    for i in range(len(pictures)):
        blurs.append(cv2.blur(pictures[i], (5, 5)))
    '''
    blur1 = cv2.blur(picture_1, (5, 5))
    blur2 = cv2.blur(picture_2, (5, 5))
    blur3 = cv2.blur(picture_3, (5, 5))
    blur4 = cv2.blur(picture_4, (5, 5))
    '''
    edges = []
    #run canny edge detector to detect edges
    for i in range(len(blurs)):
        edges.append(cv2.Canny(blurs[i], 50, 150))
    '''
    edge1 = cv2.Canny(blur1, 50, 150)
    edge2 = cv2.Canny(blur2, 50, 150)
    edge3 = cv2.Canny(blur3, 50, 150)
    edge4 = cv2.Canny(blur4, 50, 150)
    '''
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

    circle1 = cv2.HoughCircles(edges[0], cv2.HOUGH_GRADIENT,1,20,
                              param1=30, param2=30, minRadius=0, maxRadius=0)
    circle2 = cv2.HoughCircles(edges[1], cv2.HOUGH_GRADIENT,1,20,
                              param1=30, param2=30,minRadius=0,maxRadius=0)
    circle3 = cv2.HoughCircles(edges[2], cv2.HOUGH_GRADIENT,1,20,
                              param1=30,param2=30,minRadius=0,maxRadius=0)
    circle4 = cv2.HoughCircles(edges[3], cv2.HOUGH_GRADIENT,1,20,
                              param1=30,param2=30,minRadius=0,maxRadius=0)
                              
    circles1 = np.uint16(np.around(circle1))
    circles2 = np.uint16(np.around(circle2))
    circles3 = np.uint16(np.around(circle3))
    circles4 = np.uint16(np.around(circle4))
    for i in circles1[0,:]:
        # draw the outer circle
        cv2.circle(picture_1, (i[0],i[1]), i[2], (0, 255 ,0), 2)
        # draw the center of the circle
        cv2.circle(picture_1, (i[0], i[1]), 2,(0, 0, 255), 3)

    for i in circles2[0,:]:
        # draw the outer circle
        cv2.circle(picture_2, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # draw the center of the circle
        cv2.circle(picture_2, (i[0], i[1]), 2, (0, 0, 255), 3)

    for i in circles3[0,:]:
        # draw the outer circle
        cv2.circle(picture_3, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # draw the center of the circle
        cv2.circle(picture_3, (i[0], i[1]), 2, (0, 0, 255), 3)

    for i in circles4[0,:]:
        # draw the outer circle
        cv2.circle(picture_4,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(picture_4,(i[0],i[1]),2,(0,0,255),3)


    #cv2.imshow("Mask", mask)
    cv2.imshow("Candy1", picture_1)
    cv2.imshow("Candy2", picture_2)
    cv2.imshow("Candy3", picture_3)
    cv2.imshow("Candy4", picture_4)
    
    cv2.imshow("Edge1", edges[0])
    cv2.imshow("Edge2", edges[1])
    cv2.imshow("Edge3", edges[2])
    cv2.imshow("Edge4", edges[3])

    cv2.waitKey(0)
    cv2.destroyAllWindows()

main()