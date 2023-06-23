from cvzone.HandTrackingModule import HandDetector
import cv2
import cvzone
import numpy as np
from pynput.keyboard import Key, Controller

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(detectionCon=0.5, maxHands=1)
keyboard = Controller()

def drawAll(img, button):
     imgNew = np.zeros_like(img, np.uint8)
     x, y = button.pos
     cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]), 20, rt=0)
     cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]),(10, 10, 10), cv2.FILLED)
     cv2.putText(imgNew, button.text, (x + 40, y + 60), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 4)

     out = img.copy()
     alpha = 0.5
     mask = imgNew.astype(bool)
     out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
     return out

class Button():
    def __init__(self, pos, text, size=[250, 250]):
        self.pos = pos
        self.size = size
        self.text = text
    
myButton3 = Button([500, 250], "center")

while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    hands, img = detector.findHands(img)
    img = drawAll(img, myButton3)
    
    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        bbox = hand["bbox"]
        centerPoint = hand['center']
        handType = hand["type"]

        print(lmList)


        '''
        if centerPoint[1]<300 and centerPoint[0]>300 and centerPoint[0]<700:
            keyboard.press(Key.up)
            print("up")
        if centerPoint[1]>400 and centerPoint[0]>300 and centerPoint[0]<700:
            keyboard.press(Key.down)
            print("down")
        if centerPoint[0]<300 and centerPoint[1]>300 and centerPoint[1]<700:
            keyboard.press(Key.left)
            print("left")
        if centerPoint[0]>700 and centerPoint[1]>300 and centerPoint[1]<700:
            keyboard.press(Key.right)
            print("right")
        '''

    cv2.imshow("Image", img)
    cv2.waitKey(1)
    
cap.release("q")
cv2.destroyAllWindows()