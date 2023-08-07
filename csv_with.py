
from dependencies.posemodule import PoseDetector
import cv2
import math
import csv
from datetime import datetime
from stopwatch import Stopwatch

Time = datetime.now().strftime("%H:%M:%S")
Date = datetime.now().strftime("%Y-%m-%d")




#function for calling angle
def Angle(p1, p2, p3):  
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))

    if angle < 0:
        angle += 360

    return angle


#function for updating lines as angles moves
def rotate_point(x, y, cx, cy, angle):
    angle_rad = math.radians(angle)
    x_rotated = int((x - cx) * math.cos(angle_rad) + (y - cy) * math.sin(angle_rad) + cx)
    y_rotated = int(-(x - cx) * math.sin(angle_rad) + (y - cy) * math.cos(angle_rad) + cy)
    return [x_rotated, y_rotated]

#colors for lines
red = (0,0,255)
green = (0,255,0)
blue = (255,0,0)
black = (0,0,0)

#CV2 setup
cap = cv2.VideoCapture(0)
detector = PoseDetector()
cap.set(3,1280)
cap.set(4,720)

time1 = time.time()
    
while True:

    Time = datetime.now().strftime("%H:%M:%S")

    success, img = cap.read()
    img = cv2.flip(img,1)
    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False)
    if bboxInfo:
        center = bboxInfo["center"]
        cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)

    if lmList:
        #right shoulder landmark
        rightShoulder = lmList[11][1:3]
        leftShoulder = lmList[12][1:3]
        start = [rightShoulder[0] - 100, rightShoulder[1] - 100]
        #angle between shoulder points and 45-degree point i.e start
        A = Angle(leftShoulder, rightShoulder, start)
        
        #updated points for moving lines
        north_east = rotate_point(rightShoulder[0] + 1000, rightShoulder[1] - 1000, rightShoulder[0], rightShoulder[1], A-45)
        south_east = rotate_point(rightShoulder[0] + 1000, rightShoulder[1] + 1000, rightShoulder[0], rightShoulder[1], A-45)
        south_west = rotate_point(rightShoulder[0] - 1000, rightShoulder[1] + 1000, rightShoulder[0], rightShoulder[1], A-45)
        north_west = rotate_point(rightShoulder[0] - 1000, rightShoulder[1] - 1000, rightShoulder[0], rightShoulder[1], A-45)

        #distance between right and left shoulder
        dist = detector.findDistance(11,12,img,draw=True)
        dist = dist[0]

        #circle
        img = cv2.circle(img, rightShoulder, int(3/2*dist), (255, 255, 255), 3)
        
        #drawing lines 
        img = cv2.line(img, rightShoulder, north_east, blue, 2)  #north-east line
        img = cv2.line(img, rightShoulder, south_east, green, 2) #south-east line
        img = cv2.line(img, rightShoulder, south_west, black, 2) #south-west line
        img = cv2.line(img, rightShoulder, north_west, red, 2)   #north-west line

        landmark = lmList[19][1:3]
        angle_LM = Angle(north_east, rightShoulder, landmark)

        circle_bound = (landmark[0]-rightShoulder[0])**2 + (landmark[1]-rightShoulder[1])**2 > int(3/2*dist)**2
        Position = None


        if circle_bound:
            if angle_LM > 0 and angle_LM < 90:
                print("Right")
                Position = "Right"

            if angle_LM > 90 and angle_LM < 180:
                print("Down")
                Position = "Down"

            if angle_LM > 180 and angle_LM < 270:
                print("Left")
                Position = "Left"

            if angle_LM > 270 and angle_LM < 360:
                print("Up")
                Position = "Up"

        distance = ((rightShoulder[0]-landmark[0])**2 + (rightShoulder[1]-landmark[1]))**0.5
        time2 = time.time()
        stop_watch = time2 - time1
        
        with open("patient.csv", 'a',newline='') as f:
            data = csv.writer(f)
            header = ["Date","Time","stop-watch","x-coordinate","y-coordinate","Distance","Position"]
            data.writerow([Date,Time,stop_watch,landmark[0],landmark[1],distance,Position])
                

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release("q")
cv2.destroyAllWindows()