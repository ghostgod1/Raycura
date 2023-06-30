from dependencies.handtraking import HandDetector
import cv2
import numpy as np
from pynput.keyboard import Key, Controller

option = int(input("Enter option"))

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(detectionCon=0.5, maxHands=1)
keyboard = Controller()

def drawAll(img):
    imgNew = np.zeros_like(img, np.uint8)
    cv2.rectangle(img, (110, 90), (1170, 630) ,(255, 0, 0), 3)
    cv2.line(img , (110+353, 90), (110+353, 630), (0, 255, 0), 3)
    cv2.line(img, (110+353+353, 90), (110+353+353, 630), (0, 255, 0), 3)
    cv2.line(img, (110, 90+180), (1170, 90+180), (0, 255, 0), 3)
    cv2.line(img, (110, 90+180+180), (1170, 90+180+180), (0, 255, 0), 3)
    cv2.line(img, (1170, 90), (1280, 0), (0, 255, 0), 3)
    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
    return out


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)
    img = drawAll(img)

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        bbox = hand["bbox"]
        centerPoint = hand['center']
        handType = hand["type"]


        if option == 1:
            landmark = lmList[9]
        if option == 2:
            landmark = centerPoint


        if landmark[1]<90:
            print("Out of bound from Up side")

        if landmark[0]<110: 
            print("Out of bound from Left side")

        if landmark[0]>1170:
            print("Out of bound from right side")

        if landmark[0]>1170 and landmark[1] < (630-(landmark[0]-1170)):
            print("Out of bound from Right side")

        if landmark[1]>630:
            print("Out of bound from bottom side")

        if landmark[0] > 110 and landmark[0] < 463 and landmark[1] > 90 and landmark[1] < 270:
            print("1")

        if landmark[0] > 463 and landmark[0] < 463 + 353 and landmark[1] > 90 and landmark[1] < 270:
            #keyboard.press(Key.up)
            print("2")

        if landmark[0] > 463 + 353 and landmark[0] < 463 + 353 + 353 and landmark[1] > 90 and landmark[1] < 270:
            print("3")

        if landmark[0] > 110 and landmark[0] < 463 and landmark[1] > 270 and landmark[1] < 270 + 180:
            #keyboard.press(Key.left)
            print("4")

        if landmark[0] > 464 and landmark[0] < 463 + 353 and landmark[1] > 270 and landmark[1] < 270 + 180:
            print("5")

        if landmark[0] > 463 + 353 and landmark[0] < 463 + 353 + 353 and landmark[1] > 270 and landmark[1] < 270 + 180:
            #keyboard.press(Key.right)
            print("6")

        if landmark[0] > 110 and landmark[0] < 463 and landmark[1] > 450 and landmark[1] < 450 + 180:
            print("7")

        if landmark[0] > 464 and landmark[0] < 463 + 353 and landmark[1] > 450 and landmark[1] < 450 + 180:
            #keyboard.press(Key.down)
            print("8")

        if landmark[0] > 463 + 353 and landmark[0] < 463 + 353 + 353 and landmark[1] > 450 and landmark[1] < 450 + 180:
            print("9")
         
    cv2.imshow("Image", img) 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
      
cap.release("q")
cv2.destroyAllWindows()