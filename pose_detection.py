import cv2
import cvzone
import numpy as np
from cvzone.PoseModule import PoseDetector

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = PoseDetector

while True:
    success, img = cap.read()
    img = cv2.flip(img,1)

    pose, img = detector.findPose(img)

    cv2.imshow("Image", img)
    cv2.waitKey(1)