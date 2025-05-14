import cv2
import mediapipe as mp
import numpy as np

# Initialize Mediapipe Hands module
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# OpenCV video capture
cap = cv2.VideoCapture(0)

# Variables to store the last detected shape
circle_detected = False
chakra_name = ""
path = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            index_finger_tip = hand_landmarks.landmark[8]
            h, w, _ = frame.shape
            x, y = int(index_finger_tip.x * w), int(index_finger_tip.y * h)
            path.append((x, y))
            
            # Draw the path
            for i in range(1, len(path)):
                cv2.line(frame, path[i-1], path[i], (0,0, 255),2)
            
            # Check if a circle is formed
            if len(path) > 30:
                contour = np.array(path, dtype=np.int32)
                perimeter = cv2.arcLength(contour, closed=True)
                area = cv2.contourArea(contour)
                if perimeter > 100 and area > 500:
                    circle_detected = True
                    chakra_name = "Root Chakra"
    
    # Display Chakra Name if detected
    if circle_detected:
        cv2.putText(frame, chakra_name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0, 255),2)
    
    cv2.imshow("Chakra Drawing", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
