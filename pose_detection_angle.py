from dependencies.posemodule import posedetector
import cv2

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
#detector = PoseDetector()
angle = posedetector()

while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    img = angle.findPose(img)
    lmList, bboxInfo = angle.findPosition(img, bboxWithHands=False)
    if bboxInfo:
        center = bboxInfo["center"]
        cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)

        #print(lmList)
    if lmList:
        a = angle.findAngle(img, 11, 13,15)
        b = angle.findAngle(img, 13, 11, 23)

        d = angle.findDistance(11, 13, img)

        print(d)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()