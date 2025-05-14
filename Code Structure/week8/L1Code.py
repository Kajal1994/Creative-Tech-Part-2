import cv2
import mediapipe as mp
import pygame
import math

# Initialize mixer
pygame.mixer.init()
is_playing = False  # Sound status flag

# Hand detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
draw = mp.solutions.drawing_utils

# Webcam start
cap = cv2.VideoCapture(0)

# Function to calculate distance between 2 points
def get_distance(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    gesture_detected = False

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)

            h, w, _ = img.shape
            thumb_tip = hand.landmark[4]
            index_tip = hand.landmark[8]

            x1, y1 = int(thumb_tip.x * w), int(thumb_tip.y * h)
            x2, y2 = int(index_tip.x * w), int(index_tip.y * h)

            dist = get_distance(x1, y1, x2, y2)

            if dist < 30:
                gesture_detected = True
                cv2.putText(img, "Gyan Mudra - Sound Playing", (10, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Play or Stop sound based on gesture detection
    if gesture_detected and not is_playing:
        pygame.mixer.music.load("Aum.mp3")
        pygame.mixer.music.play(-1)
        is_playing = True
    elif not gesture_detected and is_playing:
        pygame.mixer.music.stop()
        is_playing = False

    cv2.imshow("Gyan Mudra Sound Control", img)

    # Exit on ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
