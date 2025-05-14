import cv2
import mediapipe as mp

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Open webcam
cap = cv2.VideoCapture(0)

# Function to detect the specific gesture
def detect_gesture(hand_landmarks):
    fingers = []

    # Thumb: Check if the tip of the thumb is close to the tip of the ring finger
    thumb_tip = hand_landmarks.landmark[4]
    ring_tip = hand_landmarks.landmark[16]
    distance_thumb_ring = abs(thumb_tip.x - ring_tip.x) + abs(thumb_tip.y - ring_tip.y)
    if distance_thumb_ring < 0.05:  # Adjust threshold for proximity
        fingers.append(1)  # Thumb touching ring finger
    else:
        fingers.append(0)

    # Index, Middle, Ring, and Pinky fingers (compare tip and lower joint)
    finger_tips = [8, 12, 16, 20]
    for i, tip in enumerate(finger_tips):
        if i == 2:  # Skip ring finger (index 2 in `finger_tips`)
            fingers.append(0)  # Ring finger is folded
        else:
            if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
                fingers.append(1)  # Finger extended
            else:
                fingers.append(0)

    # Check if gesture matches (Index, middle, pinky extended; ring folded touching thumb)
    if fingers == [1, 1, 1, 0, 1]:
        return "Sacral Chakra Activated"
    else:
        return "Unknown Gesture"

# Start processing video feed
with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert BGR to RGB for MediaPipe processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        # Flip image horizontally for better user experience
        frame = cv2.flip(frame, 1)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Detect the gesture
                chakra_name = detect_gesture(hand_landmarks)

                # Display the corresponding chakra name
                cv2.putText(frame, chakra_name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2)

        # Show video feed
        cv2.imshow("Hand Gesture Recognition", frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
