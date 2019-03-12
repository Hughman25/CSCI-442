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
    if((red >= 0 and red <= 140) and (green >= 140 and green <= 255) and (blue <= 217 and blue >= 26)):
        red = 49
        green = 172
        blue = 85
        color = "green"
    #force red
    elif((red <= 255 and red >= 165) and (green <= 140 and green >= 15) and (blue <= 180 and blue >= 0)):
        red = 177
        green = 18
        blue = 36
        color = "red"
    #force blue
    elif((red <= 75 and red >= 0) and (green <= 235 and green >= 120) and (blue <= 255 and blue >= 185)):
        red = 47
        green = 159
        blue = 215
        color = "blue"
    #force orange
    elif((red <= 255 and red >= 180) and (green <= 200 and green >= 70) and (blue >= 10 and blue <= 175)):
       red = 242
       green = 111
       blue = 34
       color = "orange"
    #force yellow
    elif((red <= 255 and red >= 200) and (green >= 200 and green <= 255) and (blue >= 0 and blue <= 137)):
        red = 255
        green = 242
        blue = 0
        color = "yellow"
    #force brown
    elif((red >= 0 and red <= 140) and (green >= 0 and green <= 160) and (blue <= 175 and blue >= 0)):
        red = 96
        green = 58
        blue = 52
        color = "brown"
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
    picture_1 = cv2.imread("candyBigSmallerTiny.jpg", cv2.IMREAD_COLOR)
    pictures = [picture_1]#, picture_2, picture_3, picture_4]

    #width, height, _ = picture_1.shape
    width = 600
    height = 800
    #initialize black frames for force color
    res1 = np.zeros((height, width, 3), np.uint8)
    res1[:, 0:width//2] = (0, 0, 0)      # (B, G, R)
    res1[:, width//2:width] = (0, 0, 0)

    blurs = (cv2.GaussianBlur(picture_1, (5, 5), 1))

    #edges = []
    #run canny edge detector to detect edges
    #for i in range(len(blurs)):
    edges = (cv2.Canny(blurs, 208, 135))
    #create named windows
    cv2.namedWindow("Candy1", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Edge1", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Res1", cv2.WINDOW_NORMAL)

    #move named windows 
    cv2.moveWindow("Candy1", 0, 0)
    cv2.moveWindow("Edge1", 400, 0)

    #initialize r,g,b,y,o,br values
    circle1 = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, 35, param1=1, param2=6, minRadius=8, maxRadius=18)
    
    circles1 = np.uint16(np.around(circle1))
    #save the y,x locations of the center of a circle
    circleLocations1 = []
    for i in circles1[0, :]:
        # draw the outer circle
        cv2.circle(edges, (i[0], i[1]), i[2] - 5, (255, 255, 255), -1)
        #save the location of the circles
        circleLocations1.append((i[0],i[1]))
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
    
    cv2.imshow("Candy1", picture_1)
    cv2.imshow("Edge1", edges)
    cv2.imshow("Res1", res1)


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