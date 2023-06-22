import cv2
import mediapipe as mp
import time

mp_hand = mp.solutions.hands
hands = mp_hand.Hands()
mp_drawing_utils = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

cap = cv2.VideoCapture(0)

prev_time = 0

while True:
    success, img = cap.read()

    if not success:
        break

    result = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    #print(result.multi_hand_landmarks)

    '''

    if result.multi_hand_landmarks:
        for hand_landmark in result.multi_hand_landmarks:
            mp_drawing_utils.draw_landmarks(
                img, 
                hand_landmark, 
                mp_hand.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
                )
            
        for id, landmark in enumerate(hand_landmark.landmark):
            #print(id, landmark)

            h, w, c = img.shape

            cx, cy = int(landmark.x*w), int(landmark.y*h)

            cv2.putText(img, str(id), (cx, cy), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,255),1)
            #print(cx, cy)


    '''
    if result.multi_hand_landmarks:

        if x< result[8][0] < x+w:


    

    cur_time = time.time()
    FPS = int(1/(cur_time - prev_time))
    prev_time = cur_time

    cv2.putText(img, f"FPS: {str(FPS)}", (100,100), cv2.FONT_HERSHEY_COMPLEX, 2, (200,200,200), 3)

    # Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)
cap.release("q")
cv2.destroyAllWindows()