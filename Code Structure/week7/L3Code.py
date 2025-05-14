import cv2
import mediapipe as mp
from pygame import mixer

# Initialize MediaPipe and Pygame mixer
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils
mixer.init()

# Load the audio
mixer.music.load("rain.wav")

# Start video capture
cap = cv2.VideoCapture(0)
is_playing = False

def fingers_up(hand_landmarks):
    fingers = []

    # Tip landmarks for index and middle fingers
    tip_ids = [8, 12]

    # Check for each finger
    for i in tip_ids:
        # Tip y should be less than pip y (folded fingers)
        if hand_landmarks.landmark[i].y < hand_landmarks.landmark[i - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingers = fingers_up(hand_landmarks)

            if fingers == [1, 0]:  # Only index finger up
                cv2.putText(frame, "Playing Audio", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                if not is_playing:
                    mixer.music.play(-1)
                    is_playing = True

            elif fingers == [1, 1]:  # Index + Middle finger up
                cv2.putText(frame, "Stopping Audio", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                if is_playing:
                    mixer.music.stop()
                    is_playing = False

    cv2.imshow("Gesture Controlled Audio", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
