from dependencies.posemodule import posedetector
import cv2
import math

#Mediapipe class calls
poseDetect = posedetector()

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
cap.set(3,1280)
cap.set(4,720)

while True:
    success, img = cap.read()
    img = cv2.flip(img,1)

    #Pose Detection
    img = poseDetect.findPose(img)
    lmListPose = poseDetect.findPosition(img, bboxWithHands=False)
    
    if lmListPose:
        #right shoulder landmark
        rightShoulder = lmListPose[11][1:3]
        leftShoulder = lmListPose[12][1:3]

        start = [rightShoulder[0] - 100, rightShoulder[1] - 100]
        #angle between shoulder points and 45-degree point i.e start
        A = Angle(leftShoulder, rightShoulder, start)
        

        #updated points for moving lines
        north_east = rotate_point(rightShoulder[0] + 1000, rightShoulder[1] - 1000, rightShoulder[0], rightShoulder[1], A-45)
        south_east = rotate_point(rightShoulder[0] + 1000, rightShoulder[1] + 1000, rightShoulder[0], rightShoulder[1], A-45)
        south_west = rotate_point(rightShoulder[0] - 1000, rightShoulder[1] + 1000, rightShoulder[0], rightShoulder[1], A-45)
        north_west = rotate_point(rightShoulder[0] - 1000, rightShoulder[1] - 1000, rightShoulder[0], rightShoulder[1], A-45)

        #circle
        img = cv2.circle(img, rightShoulder, 150, (255, 255, 255), 3)
        
        #drawing lines 
        img = cv2.line(img, rightShoulder, north_east, blue, 2)  #north-east line
        img = cv2.line(img, rightShoulder, south_east, green, 2) #south-east line
        img = cv2.line(img, rightShoulder, south_west, black, 2) #south-west line
        img = cv2.line(img, rightShoulder, north_west, red, 2)   #north-west line



        #point = [rightShoulder[0]+100, rightShoulder[1]-100]

        landmark = lmListPose[19][1:3]

        angle_NE = Angle(north_east, rightShoulder, north_east)   #0 deg / 360 deg
        angle_SE = Angle(north_east, rightShoulder, south_east)   #90 deg
        angle_SW = Angle(north_east, rightShoulder, south_west)   #180 deh
        angle_NW = Angle(north_east, rightShoulder, north_west)   #270 deg

        angle_LM = Angle(north_east, rightShoulder, landmark)

        circle_bound = (landmark[0]-rightShoulder[0])**2 + (landmark[1]-rightShoulder[1])**2 > 150**2

        if circle_bound:
            if angle_LM > angle_NE and angle_LM < angle_SE:
                print("Right")
            if angle_LM < angle_SW and angle_LM > angle_SE:
                print("Down")
            if angle_LM < angle_NW and angle_LM > angle_SW:
                print("Left")
            if angle_LM < 360 - angle_NE and angle_LM > angle_NW:
                print("Up")

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release("q")
cv2.destroyAllWindows()