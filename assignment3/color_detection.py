import cv2
import numpy as np



def main():

    picture_1 = cv2.imread('candy1.jpg') # ,0 loads image in as grayscale
    picture_2 = cv2.imread('candy2.jpg')
    cv2.imshow("Candy", picture_1)
    cv2.imshow("Candy 2", picture_2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()





main()