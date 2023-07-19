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

    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))

    if angle < 0:
        angle += 360

    return angle



def rotate_point(x, y, cx, cy, angle):
    angle_rad = math.radians(angle)
    x_rotated = int((x - cx) * math.cos(angle_rad) + (y - cy) * math.sin(angle_rad) + cx)
    y_rotated = int(-(x - cx) * math.sin(angle_rad) + (y - cy) * math.cos(angle_rad) + cy)
    return [x_rotated, y_rotated]


while True:
    success, img = cap.read()
    img = cv2.flip(img,1)

    #Pose Detection
    img = poseDetect.findPose(img)
    lmListPose = poseDetect.findPosition(img, bboxWithHands=False)
    
    if lmListPose:
        rightShoulder = lmListPose[11][1:3]

        start = [rightShoulder[0] - 100, rightShoulder[1] - 100]
        A = Angle(12, 11, start)
        
        c = rotate_point(rightShoulder[0] + 1000, rightShoulder[1] - 1000,rightShoulder[0],rightShoulder[1], A-45)
        d = rotate_point(rightShoulder[0] - 1000, rightShoulder[1] + 1000,rightShoulder[0],rightShoulder[1], A-45)
        e = rotate_point(rightShoulder[0] + 1000, rightShoulder[1] + 1000,rightShoulder[0],rightShoulder[1], A-45)
        s = rotate_point(rightShoulder[0] - 1000, rightShoulder[1] - 1000,rightShoulder[0],rightShoulder[1], A-45)

        img = cv2.circle(img, rightShoulder, 150, (255, 0, 0), 3)
        
        img = cv2.line(img, rightShoulder, s, (0, 150, 255), 2)
        img = cv2.line(img, rightShoulder, e, (0, 255, 255), 2)
        img = cv2.line(img, rightShoulder, c, (255, 0, 255), 2)
        img = cv2.line(img, rightShoulder, d, (0, 100, 200), 2)

       
    #Hand Detection
        hands, img = handDetect.findHands(img)
        if hands:
            hand = hands[0]
            lmList = hand["lmList"]

            landmark = lmList[9]

            if(s[0] == rightShoulder[0]):
                s[0] = s[0] + 1
            if(s[1] == rightShoulder[1]):
                s[1] = s[1] + 1

            if(e[0] == rightShoulder[0]):
                e[0] = e[0] + 1
            if(e[1] == rightShoulder[1]):
                e[1] = e[1] + 1

            if(c[0] == rightShoulder[0]):
                c[0] = c[0] + 1
            if(c[1] == rightShoulder[1]):
                c[1] = c[1] + 1

            if(d[0] == rightShoulder[0]):
                d[0] = d[0] + 1
            if(d[1] == rightShoulder[1]):
                d[1] = d[1] + 1
            

            l1_y = ((landmark[0] - s[0])/(s[0] - rightShoulder[0])) * (s[1] - rightShoulder[1]) + s[1]
            l1_x = ((landmark[1] - s[1])/(s[1] - rightShoulder[1])) * (s[0] - rightShoulder[0]) + s[0]

            l2_y = ((landmark[0] - rightShoulder[0])/(rightShoulder[0] - e[0])) * (rightShoulder[1] - e[1]) + rightShoulder[1]
            l2_x = ((landmark[1] - rightShoulder[1])/(rightShoulder[1] - e[1])) * (rightShoulder[0] - e[0]) + rightShoulder[0]

            l3_y = ((landmark[0] - c[0])/(c[0] - rightShoulder[0])) * (c[1] - rightShoulder[1]) + c[1]
            l3_x = ((landmark[1] - c[1])/(c[1] - rightShoulder[1])) * (c[0] - rightShoulder[0]) + c[0]
            
            l4_y = ((landmark[0] - rightShoulder[0])/(rightShoulder[0] - d[0])) * (rightShoulder[1] - d[1]) + rightShoulder[1]
            l4_x = ((landmark[1] - rightShoulder[1])/(rightShoulder[1] - d[1])) * (rightShoulder[0] - d[0]) + rightShoulder[0]


            circle_bound = (landmark[0]-rightShoulder[0])**2 + (landmark[1]-rightShoulder[1])**2 > 150**2
            
            if circle_bound:
                if landmark[0] > rightShoulder[0] and landmark[1] < l2_y and landmark[1] > l4_y:
                    print("Right side")
        
            if circle_bound:
                if landmark[0] < rightShoulder[0] and landmark[1] > l1_y and landmark[1] < l3_y:
                    print("Left side")
    
            if circle_bound:
                if landmark[1] < rightShoulder[1] and landmark[0] > l1_x and landmark[0] < l4_x:
                    print("Up side")
        
            if circle_bound:
                if landmark[1] > rightShoulder[1] and landmark[0] < l2_x and landmark[0] > l3_x:
                    print("Down side")

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release("q")
cv2.destroyAllWindows()