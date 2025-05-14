import cv2
import mediapipe as mp
import time

# Initialize MediaPipe hand tracking
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Define chakra colors and corresponding finger numbers
chakras = {
    1: ("Root Chakra (Red)", (0, 0, 255)),  # Red
    2: ("Sacral Chakra (Orange)", (0, 165, 255)),  # Orange
    3: ("Solar Plexus Chakra (Yellow)", (0, 255, 255)),  # Yellow
    4: ("Heart Chakra (Green)", (0, 255, 0)),  # Green
    5: ("Throat Chakra (Blue)", (255, 0, 0)),  # Blue
}

# Start webcam
cap = cv2.VideoCapture(0)
last_guess_time = time.time()  # Track last correct guess time

def count_fingers(landmarks):
    """Counts the number of extended fingers based on MediaPipe hand landmarks."""
    finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
    count = 0

    for tip in finger_tips:
        if landmarks[tip].y < landmarks[tip - 2].y:  # If tip is above the lower joint
            count += 1

    # Thumb detection (if thumb is open)
    if landmarks[4].x < landmarks[3].x:  
        count += 1

    return count

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Mirror image for better user interaction
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hands
    result = hands.process(rgb_frame)
    fingers_detected = None

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingers_detected = count_fingers(hand_landmarks.landmark)

        if fingers_detected is not None and fingers_detected in chakras:
            chakra_name, chakra_color = chakras[fingers_detected]
            cv2.putText(frame, f"Chakra: {chakra_name}", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                        color=chakra_color, thickness=2)
            cv2.putText(frame, f"Fingers: {fingers_detected}", (50, h - 150),
                        cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                        color=(255, 255, 255), thickness=2)

            # Check if guess is correct
            if time.time() - last_guess_time > 1.5:  
                last_guess_time = time.time()  
        else:
            cv2.putText(frame,
                        "No corresponding chakra",
                        (50, h - 50),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1.5,
                        color=(200), thickness=3)

    else:
        cv2.putText(frame,
                    "No hands detected",
                    (50, h - 50),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1.5,
                    color=(200), thickness=3)

    # Show video feed with updates
    cv2.imshow("Chakra Guessing", frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
