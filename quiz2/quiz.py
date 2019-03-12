import cv2
import numpy as np

def main():
    picture_1 = cv2.imread("facePic.jpg", cv2.IMREAD_COLOR)
    face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_eye.xml')
    height, width, depth = picture_1.shape
    picture_2 = np.zeros((height, width, 3), np.uint8)
    picture_2[:, 0:width//2] = (30, 30, 30)      # (B, G, R)
    picture_2[:, width//2:width] = (30, 30, 30)
    picture_3 = cv2.subtract(picture_1, picture_2)
    gray = cv2.cvtColor(picture_3, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.5, 5)
    print(faces)
    for (x,y,w,h) in faces:
        cv2.rectangle(picture_3,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = picture_3[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    cv2.putText(picture_3, "CSCI 442 matthew Sagen", (5, 780), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.namedWindow("Matthew Sagen", cv2.WINDOW_KEEPRATIO)
    cv2.moveWindow("Matthew Sagen", 0, 0)

    cv2.imshow("Matthew Sagen", picture_3)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
main()