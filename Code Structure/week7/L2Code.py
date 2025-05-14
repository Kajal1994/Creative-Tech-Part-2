import cv2
import mediapipe as mp
import pygame

# Initialize Pygame mixer
pygame.mixer.init()
pygame.mixer.music.load("A.wav")  # Replace with your chakra sound file
pygame.mixer.music.play(-1)  # Loop the sound

# MediaPipe setup
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp.solutions.hands.Hands(min_detection_confidence=0.7)

# Webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Flip the frame and convert to RGB
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    h, w, _ = frame.shape
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Use the wrist point (landmark 0) to track hand position
            wrist_y = hand_landmarks.landmark[0].y

            # Map wrist Y-position to volume
            # Y = 0 (top) → 1.0 volume, Y = 1 (bottom) → 0.0 volume
            volume = 1.0 - wrist_y
            volume = max(0.0, min(volume, 1.0))  # Clamp between 0 and 1

            pygame.mixer.music.set_volume(volume)

            cv2.putText(frame, f"Volume: {volume:.2f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Gesture-Controlled Volume", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.music.stop()
