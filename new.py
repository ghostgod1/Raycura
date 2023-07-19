from dependencies.handtraking import HandDetector
from dependencies.posemodule import posedetector
import cv2
import math

#CV2 setup
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

#Mediapipe class calls
handDetect = HandDetector(detectionCon=0.5, maxHands=1)
poseDetect = posedetector()

#function for calling angle
def Angle(p1, p2, p3):  
    x1, y1 = lmListPose[p1][1:3]
    x2, y2 = lmListPose[p2][1:3]
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

red = (0,0,255)
green = (0,255,0)
blue = (255,0,0)
black = (0,0,0)


while True:
    success, img = cap.read()
    img = cv2.flip(img,1)

    #Pose Detection
    img = poseDetect.findPose(img)
    lmListPose = poseDetect.findPosition(img, bboxWithHands=False)
    
    if lmListPose:
        #right shoulder landmark
        rightShoulder = lmListPose[11][1:3]

        start = [rightShoulder[0] - 100, rightShoulder[1] - 100]
        #angle between shoulder points and 45-degree point i.e start
        A = Angle(12, 11, start)
        

        #updated points for moving lines
        north_east = rotate_point(rightShoulder[0] + 1000, rightShoulder[1] - 1000,rightShoulder[0],rightShoulder[1], A-45)
        south_east = rotate_point(rightShoulder[0] + 1000, rightShoulder[1] + 1000,rightShoulder[0],rightShoulder[1], A-45)
        south_west = rotate_point(rightShoulder[0] - 1000, rightShoulder[1] + 1000,rightShoulder[0],rightShoulder[1], A-45)
        north_west = rotate_point(rightShoulder[0] - 1000, rightShoulder[1] - 1000,rightShoulder[0],rightShoulder[1], A-45)

        #circle
        img = cv2.circle(img, rightShoulder, 150, (255, 255, 255), 3)
        
        #drawing lines 
        img = cv2.line(img, rightShoulder, north_east, blue, 2)  #north-east line
        img = cv2.line(img, rightShoulder, south_east, green, 2) #south-east line
        img = cv2.line(img, rightShoulder, south_west, black, 2) #south-west line
        img = cv2.line(img, rightShoulder, north_west, red, 2)   #north-west line

       
        #Hand Detection
        hands, img = handDetect.findHands(img)
        if hands:
            hand = hands[0]
            lmList = hand["lmList"]

            #Hand landmark below middle finger
            landmark = lmList[9]

            #code to avoid division by zero error
            if(north_west[0] == rightShoulder[0]):
                north_west[0] = north_west[0] + 1
            if(north_west[1] == rightShoulder[1]):
                north_west[1] = north_west[1] + 1

            if(south_east[0] == rightShoulder[0]):
                south_east[0] = south_east[0] + 1
            if(south_east[1] == rightShoulder[1]):
                south_east[1] = south_east[1] + 1

            if(north_east[0] == rightShoulder[0]):
                north_east[0] = north_east[0] + 1
            if(north_east[1] == rightShoulder[1]):
                north_east[1] = north_east[1] + 1

            if(south_west[0] == rightShoulder[0]):
                south_west[0] = south_west[0] + 1
            if(south_west[1] == rightShoulder[1]):
                south_west[1] = south_west[1] + 1
            

            l1_y = ((landmark[0] - north_west[0])/(north_west[0] - rightShoulder[0])) * (north_west[1] - rightShoulder[1]) + north_west[1]
            l1_x = ((landmark[1] - north_west[1])/(north_west[1] - rightShoulder[1])) * (north_west[0] - rightShoulder[0]) + north_west[0]

            l2_y = ((landmark[0] - rightShoulder[0])/(rightShoulder[0] - south_east[0])) * (rightShoulder[1] - south_east[1]) + rightShoulder[1]
            l2_x = ((landmark[1] - rightShoulder[1])/(rightShoulder[1] - south_east[1])) * (rightShoulder[0] - south_east[0]) + rightShoulder[0]

            l3_y = ((landmark[0] - north_east[0])/(north_east[0] - rightShoulder[0])) * (north_east[1] - rightShoulder[1]) + north_east[1]
            l3_x = ((landmark[1] - north_east[1])/(north_east[1] - rightShoulder[1])) * (north_east[0] - rightShoulder[0]) + north_east[0]
            
            l4_y = ((landmark[0] - rightShoulder[0])/(rightShoulder[0] - south_west[0])) * (rightShoulder[1] - south_west[1]) + rightShoulder[1]
            l4_x = ((landmark[1] - rightShoulder[1])/(rightShoulder[1] - south_west[1])) * (rightShoulder[0] - south_west[0]) + rightShoulder[0]


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