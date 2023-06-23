import cv2

from dependencies.posemodule import posedetector
from dependencies.handtraking import HandDetector

detector_pose = posedetector()
detector_hand = HandDetector()

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

while True:
    success, img = cap.read()
    img = cv2.flip(img,1)

    hands, img = detector_hand.findHands(img)
    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        bbox = hand["bbox"]
        centerPoint = hand['center']
        handType = hand["type"]

    

    #if lmList_pose:
        #angle = posedetector.findAngle(img, )
    
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()