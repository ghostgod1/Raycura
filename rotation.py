from dependencies.handtraking import HandDetector
from dependencies.posemodule import posedetector
import cv2
import math

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

handDetect = HandDetector(detectionCon=0.5, maxHands=1)
poseDetect = posedetector()

def Angle(p1, p2, p3):
        
    x1, y1 = lmListPose[p1][1:3]
    x2, y2 = lmListPose[p2][1:3]
    x3, y3 = p3

    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                         math.atan2(y1 - y2, x1 - x2))
    if angle < 0:
        angle += 360

    return angle



def rotate_point(x, y, cx, cy, angle):
    angle_rad = math.radians(angle)
    x_rotated = int((x - cx) * math.cos(angle_rad) + (y - cy) * math.sin(angle_rad) + cx)
    y_rotated = int(-(x - cx) * math.sin(angle_rad) + (y - cy) * math.cos(angle_rad) + cy)
    return x_rotated, y_rotated


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
      #  A = Angle(12, 11, start)
        rightShoulder = lmListPose[11][1:3]
        leftShoulder = lmListPose[12][1:3]

        start = [rightShoulder[0] - 1000, rightShoulder[1] - 1000]
        end = [rightShoulder[0] + 1000, rightShoulder[1] + 1000]
        A = Angle(12, 11, start)
        
        start_point = [rightShoulder[0] - 100, rightShoulder[1] - 100]
        s = rotate_point(rightShoulder[0] - 1000, rightShoulder[1] - 1000,rightShoulder[0],rightShoulder[1], A-45)
        end_point = [rightShoulder[0] + 100, rightShoulder[1] + 100]
        e = rotate_point(rightShoulder[0] + 1000, rightShoulder[1] + 1000,rightShoulder[0],rightShoulder[1], A-45)
        color = (255, 0, 0)
        thickness = 2
        

        c = rotate_point(rightShoulder[0] + 1000, rightShoulder[1] - 1000, rightShoulder[0], rightShoulder[1], A-45)
        d = rotate_point(rightShoulder[0] - 1000, rightShoulder[1] + 1000,rightShoulder[0],rightShoulder[1] ,A-45)

        if c[0] == d[0]:
            f = c[0] + 1
        else:
            f = c[0]

        if c[1] == d[1]:
            ff = c[1]+1
        else:
            ff = c[1]

        if s[0] == e[0]:
            z = s[0] + 1
        else:
            z = s[0]

        if s[1] == e[1]:
            zz = s[1] + 1
        else:
            zz = s[0]
        
       


        img = cv2.circle(img, rightShoulder, 150, (255, 0, 0), 3)
        img = cv2.rectangle(img, start, end,color,thickness)
        img = cv2.line(img, start_point, end_point, color, thickness)

        img = cv2.line(img, s, (rightShoulder[0], rightShoulder[1]), (0, 0, 255), thickness)
        img = cv2.line(img, (rightShoulder[0], rightShoulder[1]), e, (0, 0, 255), thickness)
        img = cv2.line(img, c, (rightShoulder[0], rightShoulder[1]), (0, 0, 255), thickness)
        img = cv2.line(img, (rightShoulder[0], rightShoulder[1]), d, (0, 0, 255), thickness)
        #print(A)
      
    #Hand Detection
    hands, img = handDetect.findHands(img)
    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        bbox = hand["bbox"]
        centerPoint = hand['center']
        handType = hand["type"]



        landmark = lmList[9]
        circle_bound = (landmark[0]-rightShoulder[0])**2 + (landmark[1]-rightShoulder[1])**2 > 150**2
        if circle_bound:
            if landmark[0] > rightShoulder[0] and landmark[1] < (((landmark[0]-s[0])/z-e[0]) * (s[1]-e[1]) + s[1]) and landmark[1] > (((landmark[0]-c[0])/(f-d[0])) * (c[1]-d[1]) + c[1]):
                if lmListPose[0][2] < lmListPose[11][2]:
                    print("Right side")
                else:
                    print("Left side")
    
        if circle_bound:
            if landmark[0] < rightShoulder[0] and landmark[1] > (((landmark[0]-s[0])/(z-e[0])) * (s[1]-e[1]) + s[1]) and landmark[1] < (((landmark[0]-c[0])/(f-d[0])) * (c[1]-d[1]) + c[1]):
                if lmListPose[0][2] < lmListPose[11][2]:
                    print("Left side")
                else:
                    print("Right side")
 

        if circle_bound:
            if landmark[1] < rightShoulder[1] and landmark[0] > (((landmark[1]-s[1])/(zz-e[1])) * (s[0]-e[0]) + s[0]) and landmark[0] < (((landmark[1]-c[1])/(ff-d[1])) * (c[0]-d[0]) + c[0]):
                if lmListPose[0][2] < lmListPose[11][2]:
                    print("Up side")
                else:
                    print("Down side")
  
        if circle_bound:
            if landmark[1] > rightShoulder[1] and landmark[0] < (((landmark[1]-s[1])/(zz-e[1])) * (s[0]-e[0]) + s[0]) and landmark[0] > (((landmark[1]-c[1])/(ff-d[1])) * (c[0]-d[0]) + c[0]):
                if lmListPose[0][2] < lmListPose[11][2]:
                    print("Down side")
                else:
                    print("Up side")
  
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release("q")
cv2.destroyAllWindows()