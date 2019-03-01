'''
Authors: Matthew Sagen and Hugh Jackovich
'''

import cv2
import numpy as np



#helper method to get averages of surrounding pixels 
def getAverage(pic, x, y):
    #compute average red value
    red = int((int(pic[y][x][2]) + int(pic[y+1][x][2]) + 
           int(pic[y-1][x][2]) + int(pic[y][x+1][2]) + 
           int(pic[y][x-1][2]) + int(pic[y+1][x+1][2]) +
           int(pic[y-1][x-1][2]) + int(pic[y-1][x+1][2]) + int(pic[y+1][x-1][2])) / 9)
    #compute average green value
    green = int((int(pic[y][x][1]) + int(pic[y+1][x][1])+ 
           int(pic[y-1][x][1]) + int(pic[y][x+1][1]) + 
           int(pic[y][x-1][1]) + int(pic[y+1][x+1][1]) +
           int(pic[y-1][x-1][1]) + int(pic[y-1][x+1][1]) + int(pic[y+1][x-1][1])) / 9)
    #compute average blue value
    blue = int((int(pic[y][x][0]) + int(pic[y+1][x][0]) + 
           int(pic[y-1][x][0]) + int(pic[y][x+1][0]) + 
           int(pic[y][x-1][0]) + int(pic[y+1][x+1][0]) +
           int(pic[y-1][x-1][0]) + int(pic[y-1][x+1][0]) + int(pic[y+1][x-1][0])) / 9)
    return red, green, blue

#helper method to force colors within a threshold
def forceColor(red, green, blue):
    #force green
    color = "white"
    if((red >= 0 and red <= 45) and (green >= 170 and green <= 255) and (blue <= 195 and blue >= 70)):
        red = 49
        green = 172
        blue = 85
        color = "green"
    #force red
    elif((red <= 255 and red >= 170) and (green <= 140 and green >= 45) and (blue <= 180 and blue >= 60)):
        red = 177
        green = 18
        blue = 36
        color = "red"
    #force blue
    elif((red <= 35 and red >= 0) and (green <= 235 and green >= 120) and (blue <= 255 and blue >= 220)):
        red = 47
        green = 159
        blue = 215
        color = "blue"
    #force yellow
    elif((red <= 255 and red >= 200) and (green >= 200 and green <= 255) and (blue >= 0 and blue <= 170)):
        red = 255
        green = 242
        blue = 0
        color = "yellow"
    #force brown
    elif((red >= 60 and red <= 160) and (green >= 70 and green <= 200) and (blue <= 200 and blue >= 70)):
        red = 96
        green = 58
        blue = 52
        color = "brown"
    #force orange
    elif((red <= 255 and red >= 220) and (green <= 200 and green >= 90) and (blue >= 10 and blue <= 165)):
       red = 242
       green = 111
       blue = 34
       color = "orange"
    #if we miss the range keep it white
    else:
        red = 255
        green = 255
        blue = 255
        color = "white"
    return red, green, blue, color

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
    #res1 = picture_1.copy()
    width = 600
    height = 800
    #initialize black frames for force color
    res1 = np.zeros((height, width, 3), np.uint8)
    res1[:, 0:width//2] = (0, 0, 0)      # (B, G, R)
    res1[:, width//2:width] = (0, 0, 0)

    res2 = np.zeros((height, width, 3), np.uint8)
    res2[:, 0:width//2] = (0, 0, 0)      # (B, G, R)
    res2[:, width//2:width] = (0, 0, 0)

    res3 = np.zeros((height, width, 3), np.uint8)
    res3[:, 0:width//2] = (0, 0, 0)      # (B, G, R)
    res3[:, width//2:width] = (0, 0, 0)

    res4 = np.zeros((height,width,3), np.uint8)
    res4[:, 0:width//2] = (0, 0, 0)      # (B, G, R)
    res4[:, width//2:width] = (0, 0, 0)
    #blur the images with 5x5
    blurs = []
    for i in range(len(pictures)):
        blurs.append(cv2.GaussianBlur(pictures[i], (5, 5), 1))

    edges = []
    #run canny edge detector to detect edges
    for i in range(len(blurs)):
        edges.append(cv2.Canny(blurs[i], 200, 150))
    #create named windows
    cv2.namedWindow("Candy1", cv2.WINDOW_KEEPRATIO)
    cv2.namedWindow("Candy2", cv2.WINDOW_KEEPRATIO)
    cv2.namedWindow("Candy3", cv2.WINDOW_KEEPRATIO)
    cv2.namedWindow("Candy4", cv2.WINDOW_KEEPRATIO)
    cv2.namedWindow("Edge1", cv2.WINDOW_KEEPRATIO)
    cv2.namedWindow("Edge2", cv2.WINDOW_KEEPRATIO)
    cv2.namedWindow("Edge3", cv2.WINDOW_KEEPRATIO)
    cv2.namedWindow("Edge4", cv2.WINDOW_KEEPRATIO)
    cv2.namedWindow("Res1", cv2.WINDOW_KEEPRATIO)
    cv2.namedWindow("Res2", cv2.WINDOW_KEEPRATIO)
    cv2.namedWindow("Res3", cv2.WINDOW_KEEPRATIO)
    cv2.namedWindow("Res4", cv2.WINDOW_KEEPRATIO)

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


    circle1 = cv2.HoughCircles(edges[0], cv2.HOUGH_GRADIENT, 1, 35, param1=1, param2=38, minRadius=8, maxRadius=0)
    circle2 = cv2.HoughCircles(edges[1], cv2.HOUGH_GRADIENT, 1, 35, param1=1, param2=35, minRadius=8, maxRadius=0)
    circle3 = cv2.HoughCircles(edges[2], cv2.HOUGH_GRADIENT, 1, 35, param1=1, param2=35, minRadius=8, maxRadius=0)
    circle4 = cv2.HoughCircles(edges[3], cv2.HOUGH_GRADIENT, 1, 35, param1=1, param2=55, minRadius=8, maxRadius=0)
                              
    circles1 = np.uint16(np.around(circle1))
    circles2 = np.uint16(np.around(circle2))
    circles3 = np.uint16(np.around(circle3))
    circles4 = np.uint16(np.around(circle4))
    #save the y,x locations of the center of a circle
    circleLocations1 = []
    circleLocations2 = []
    circleLocations3 = []
    circleLocations4 = []
    for i in circles1[0, :]:
        # draw the outer circle
        cv2.circle(edges[0], (i[0], i[1]), i[2] - 5, (255, 255, 255), -1)
        #save the location of the circles
        circleLocations1.append((i[0],i[1]))

    for i in circles2[0, :]:
        # draw the outer circle
        cv2.circle(edges[1], (i[0], i[1]), i[2] - 5, (255, 255, 255), -1)
        #save the location of the circles
        circleLocations2.append((i[0],i[1]))
    for i in circles3[0, :]:
        # draw the outer circle
        cv2.circle(edges[2], (i[0], i[1]), i[2] - 5, (255, 255, 255), -1)
        #save the location of the circles
        circleLocations3.append((i[0], i[1]))
    for i in circles4[0, :]:
        # draw the outer circle
        cv2.circle(edges[3], (i[0], i[1]), i[2] - 5, (255, 255, 255), -1)
        #save the location of the circles
        circleLocations4.append((i[0], i[1]))
    
    #use the locations to find original color in circle
    num_red = 0
    num_green = 0
    num_blue = 0
    num_yellow = 0
    num_orange = 0
    num_brown = 0
    color = ""
    for i in range(len(circleLocations1)):
        rgb = picture_1[circleLocations1[i][1], circleLocations1[i][0]]
        red, green, blue = getAverage(picture_1, circleLocations1[i][0], circleLocations1[i][1])
        red, green, blue, color = forceColor(red, green, blue)
        cv2.circle(res1, (circleLocations1[i][0], circleLocations1[i][1]), 15, (blue, green, red), -1)
        if(color == "red"):
            num_red += 1
        elif(color == "green"):
            num_green += 1
        elif(color == "blue"):
            num_blue += 1
        elif(color == "yellow"):
            num_yellow += 1
        elif(color == "orange"):
            num_orange += 1
        elif(color == "brown"):
            num_brown += 1
    updateText(picture_1, num_red, num_green, num_blue, num_yellow, num_orange, num_brown)
    num_red = 0
    num_green = 0
    num_blue = 0
    num_yellow = 0
    num_orange = 0
    num_brown = 0
    color = ""
    for i in range(len(circleLocations2)):
        rgb = picture_2[circleLocations2[i][1], circleLocations2[i][0]]
        red, green, blue = getAverage(picture_2, circleLocations2[i][0], circleLocations2[i][1])
        red, green, blue, color = forceColor(red, green, blue)
        cv2.circle(res2, (circleLocations2[i][0], circleLocations2[i][1]), 15, (blue, green, red), -1)
        if(color == "red"):
            num_red += 1
        elif (color == "green"):
            num_green += 1
        elif (color == "blue"):
            num_blue += 1
        elif (color == "yellow"):
            num_yellow += 1
        elif (color == "orange"):
            num_orange += 1
        elif (color == "brown"):
            num_brown += 1
    updateText(picture_2, num_red, num_green, num_blue, num_yellow, num_orange, num_brown)
    num_red = 0
    num_green = 0
    num_blue = 0
    num_yellow = 0
    num_orange = 0
    num_brown = 0
    color = ""
    for i in range(len(circleLocations3)):
        rgb = picture_3[circleLocations3[i][1], circleLocations3[i][0]]
        red, green, blue = getAverage(picture_3, circleLocations3[i][0], circleLocations3[i][1])
        red, green, blue, color = forceColor(red, green, blue)
        cv2.circle(res3, (circleLocations3[i][0], circleLocations3[i][1]), 15, (blue, green, red), -1)
        if(color == "red"):
            num_red += 1
        elif (color == "green"):
            num_green += 1
        elif (color == "blue"):
            num_blue += 1
        elif (color == "yellow"):
            num_yellow += 1
        elif (color == "orange"):
            num_orange += 1
        elif (color == "brown"):
            num_brown += 1
    updateText(picture_3, num_red, num_green, num_blue, num_yellow, num_orange, num_brown)
    num_red = 0
    num_green = 0
    num_blue = 0
    num_yellow = 0
    num_orange = 0
    num_brown = 0
    color = ""
    for i in range(len(circleLocations4)):
        rgb = picture_4[circleLocations4[i][1], circleLocations4[i][0]]
        red, green, blue = getAverage(picture_4, circleLocations4[i][0], circleLocations4[i][1])
        red, green, blue, color = forceColor(red, green, blue)
        cv2.circle(res4, (circleLocations4[i][0], circleLocations4[i][1]), 15, (blue, green, red), -1)
        if(color == "red"):
            num_red += 1
        elif (color == "green"):
            num_green += 1
        elif (color == "blue"):
            num_blue += 1
        elif (color == "yellow"):
            num_yellow += 1
        elif (color == "orange"):
            num_orange += 1
        elif (color == "brown"):
            num_brown += 1
    updateText(picture_4, num_red, num_green, num_blue, num_yellow, num_orange, num_brown)

    cv2.imshow("Candy1", picture_1)
    cv2.imshow("Candy2", picture_2)
    cv2.imshow("Candy3", picture_3)
    cv2.imshow("Candy4", picture_4)
    cv2.imshow("Edge1", edges[0])
    cv2.imshow("Edge2", edges[1])
    cv2.imshow("Edge3", edges[2])
    cv2.imshow("Edge4", edges[3])
    cv2.imshow("Res1", res1)
    cv2.imshow("Res2", res2)
    cv2.imshow("Res3", res3)
    cv2.imshow("Res4", res4)


    #import video file
    cap = cv2.VideoCapture('MandMVideoSmall.mp4')

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        if ret:
            vid = cv2.cvtColor(frame, 0)

        #blur and run canny on frame
        blur = cv2.GaussianBlur(vid, (5, 5), 1)
        edge = cv2.Canny(blur, 50, 50)
        #find circles in frame
        circles = cv2.HoughCircles(edge, cv2.HOUGH_GRADIENT, 1, 35, param1=1, param2=35, minRadius=0, maxRadius=0)
        num_red = 0
        num_green = 0
        num_blue = 0
        num_yellow = 0
        num_orange = 0
        num_brown = 0
        if(circles is not None):
            circles1 = np.uint16(np.around(circles))
            circleLocations = []
            #fill in circles
            for i in circles1[0, :]:
                #save the location of the circles in the frame
                circleLocations.append((i[0], i[1]))
            #find number of colors
            color = ""
            for i in range(len(circleLocations)):
                rgb = vid[circleLocations[i][1], circleLocations[i][0]]
                red, green, blue = getAverage(vid, circleLocations[i][0], circleLocations[i][1])
                red, green, blue, color = forceColor(red, green, blue)
                if(color == "red"):
                    num_red += 1
                elif(color == "green"):
                    num_green += 1
                elif(color == "blue"):
                    num_blue += 1
                elif(color == "yellow"):
                    num_yellow += 1
                elif(color == "orange"):
                    num_orange += 1
                elif(color == "brown"):
                    num_brown += 1
        updateText(vid, num_red, num_green, num_blue, num_yellow, num_orange, num_brown)
        cv2.imshow('Video', vid)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.waitKey(0)
    cv2.destroyAllWindows()

main()