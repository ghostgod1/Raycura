from dependencies.handtraking import HandDetector
import cv2
import numpy as np
from pynput.keyboard import Key, Controller

option = int(input("Enter Option : "))

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.5, maxHands=1)
keyboard = Controller()  

def drawAll(img):
    imgNew = np.zeros_like(img, np.uint8)
    cv2.line(img, (0 ,0), (1280, 720), (0, 255, 0), 3) # from origin to bottom right
    cv2.line(img, (0, 720), (1280, 0), (0, 255, 0), 3) # bottom left to top right
    cv2.rectangle(img, (160, 90), (1120, 630), (0, 0, 255), 3)
    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
    return out



while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))
    img = cv2.flip(img , 1)
    hands, img = detector.findHands(img)
    img = drawAll(img)

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        bbox = hand["bbox"]
        centerPoint = hand['center']
        handType = hand["type"]

        if option == 1:
            centerPoint = lmList[9]
        if option == 2:
            centerPoint = centerPoint
        
        # Inner box boundaries
        if centerPoint[0] > 640 and centerPoint[0] < 1120:
            if centerPoint[0]>640 and centerPoint[1] > ((-720/1280)*centerPoint[0] +720) and centerPoint[1] < ((720/1280)*centerPoint[0]): # x co-ordinate of hand for right side
                print("Right side")
                #keyboard.press(Key.right)

        if centerPoint[0] < 640 and centerPoint[0] > 160:
            if centerPoint[0]<640 and centerPoint[1] > ((720/1280)*centerPoint[0]) and centerPoint[1] < ((-720/1280)*centerPoint[0] + 720):
                print("Left side")
                #keyboard.press(Key.left)

        if centerPoint[1] < 360 and centerPoint[1] > 90:
            if centerPoint[1]<360 and centerPoint[0] > ((1280/720)*centerPoint[1]) and centerPoint[0] < ((-1280/720)*centerPoint[1] + 1280):
                print("Up side")
                #keyboard.press(Key.up)

        if centerPoint[1] > 360 and centerPoint[1] < 630:
            if centerPoint[1]>360 and centerPoint[0] < ((1280/720)*centerPoint[1]) and centerPoint[0] > ((-1280/720)*centerPoint[1] + 1280):
                print("Down side")
                #keyboard.press(Key.down)


        # Out of bound boundaries
        if centerPoint[0] > 1120:
            if centerPoint[0]>640 and centerPoint[1] > ((-720/1280)*centerPoint[0] +720) and centerPoint[1] < ((720/1280)*centerPoint[0]): # x co-ordinate of hand for right side
                print("Out of bound from Right side")
                #keyboard.press(Key.right)

        if centerPoint[0] < 160:
            if centerPoint[0]<640 and centerPoint[1] > ((720/1280)*centerPoint[0]) and centerPoint[1] < ((-720/1280)*centerPoint[0] + 720):
                print("Out of bound from Left side")
                #keyboard.press(Key.left)

        if centerPoint[1] < 90:
            if centerPoint[1]<360 and centerPoint[0] > ((1280/720)*centerPoint[1]) and centerPoint[0] < ((-1280/720)*centerPoint[1] + 1280):
                print("Out of bound from Up side")
                #keyboard.press(Key.up)

        if centerPoint[1] > 630:
            if centerPoint[1]>360 and centerPoint[0] < ((1280/720)*centerPoint[1]) and centerPoint[0] > ((-1280/720)*centerPoint[1] + 1280):
                print("Out of bound from Down side")
                #keyboard.press(Key.down)


    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

cap.release("q")
cv2.destroyAllWindows()