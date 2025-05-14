import cv2
import mediapipe as mp
import pygame
import math

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# Initialize Pygame Mixer
pygame.mixer.init()

# Load audio files
aum_sound = pygame.mixer.Sound("Aum.mp3")
sacral_sound = pygame.mixer.Sound("Sacral.mp3")

# Track current playing gesture
current_gesture = None

# Helper function to calculate distance between two landmarks
def distance(pt1, pt2):
    return math.hypot(pt2[0] - pt1[0], pt2[1] - pt1[1])

# Start webcam feed
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    # Flip for natural interaction and convert color
    frame = cv2.flip(frame, 1)
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get landmark positions
            h, w, _ = frame.shape
            landmarks = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks.landmark]

            # Landmark indices
            thumb_tip = landmarks[4]
            index_tip = landmarks[8]
            middle_tip = landmarks[12]

            # Calculate distances
            thumb_index_dist = distance(thumb_tip, index_tip)
            thumb_middle_dist = distance(thumb_tip, middle_tip)

            # Debug distances
            print(f"Thumb-Index: {thumb_index_dist:.2f}, Thumb-Middle: {thumb_middle_dist:.2f}")

            # Gesture detection logic
            if thumb_index_dist < 40 and thumb_middle_dist > 50:
                detected_gesture = "gyan"
                cv2.putText(frame, "Root Chakra", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            elif thumb_middle_dist < 40 and thumb_index_dist > 50:
                detected_gesture = "sacral"
                cv2.putText(frame, "Sacral Chakra", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 128, 0), 2)

            else:
                detected_gesture = None
                pygame.mixer.stop()
                current_gesture = None

            # Play new sound only if gesture changed
            if detected_gesture != current_gesture:
                pygame.mixer.stop()
                if detected_gesture == "gyan":
                    aum_sound.play()
                elif detected_gesture == "sacral":
                    sacral_sound.play()
                current_gesture = detected_gesture

    else:
        # No hand detected
        pygame.mixer.stop()
        current_gesture = None

    cv2.imshow("Mudra Detection", frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
