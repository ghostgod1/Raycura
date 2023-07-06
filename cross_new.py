from dependencies.handtraking import HandDetector
from dependencies.posemodule import posedetector
import cv2
import math

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

def Angle(p1, p2, p3):
        
    x1, y1 = lmListPose[p1][1:3]
    x2, y2 = lmListPose[p2][1:3]
    x3, y3 = p3

    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                         math.atan2(y1 - y2, x1 - x2))
    if angle < 0:
        angle += 360

    return angle

handDetect = HandDetector(detectionCon=0.5, maxHands=1)
poseDetect = posedetector()

while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))
    img = cv2.flip(img,1)

    #Pose Detection
    img = poseDetect.findPose(img)
    lmListPose, bboxInfo = poseDetect.findPosition(img, bboxWithHands=False)
    if bboxInfo:
        center = bboxInfo["center"]
        cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)

        rightShoulder = lmListPose[11][1:3]

        start_point= [rightShoulder[0] - 1000, rightShoulder[1] - 1000]
        end_point = [rightShoulder[0] + 1000, rightShoulder[1] + 1000]
        color = (255, 0, 0)
        thickness = 2

        a = [rightShoulder[0]+1000, rightShoulder[1]-1000]
        b = [rightShoulder[0]-1000, rightShoulder[1]+1000]

        img = cv2.rectangle(img, start_point, end_point,color,thickness)
        img = cv2.line(img, start_point, end_point, color, thickness)
        img = cv2.line(img, a, b, color, thickness)

        print(Angle(12,11,start_point))

    #Hand Detection
    hands, img = handDetect.findHands(img)
    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        bbox = hand["bbox"]
        centerPoint = hand['center']
        handType = hand["type"]

        landmark = lmList[9]

        if landmark[0] > rightShoulder[0]:
            if landmark[0] > rightShoulder[0] and landmark[1] < (landmark[0]-rightShoulder[0]+rightShoulder[1]) and landmark[1] > (-landmark[0]+rightShoulder[0]+rightShoulder[1]):
                print("Right side")

        if landmark[0] < rightShoulder[0]:
            if landmark[0] < rightShoulder[0] and landmark[1] > (landmark[0]-rightShoulder[0]+rightShoulder[1]) and landmark[1] < (-landmark[0]+rightShoulder[0]+rightShoulder[1]):
                print("Left side")

        if landmark[1] < rightShoulder[1]:
            if landmark[1] < rightShoulder[1] and landmark[0] > (landmark[1]+rightShoulder[0]-rightShoulder[1]) and landmark[0] < (-landmark[1]+rightShoulder[0]+rightShoulder[1]):
                print("Up side")

        if landmark[1] > rightShoulder[1]:
            if landmark[1] > rightShoulder[1] and landmark[0] < (landmark[1]+rightShoulder[0]-rightShoulder[1]) and landmark[0] > (-landmark[1]+rightShoulder[0]+rightShoulder[1]):
                print("Down side")

    

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release("q")
cv2.destroyAllWindows()