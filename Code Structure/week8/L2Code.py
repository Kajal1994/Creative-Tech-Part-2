import cv2
import mediapipe as mp
import pygame

# Initialize MediaPipe and Pygame
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
pygame.mixer.init()
pygame.mixer.music.load("Aum.mp3")  # Replace with your audio file

cap = cv2.VideoCapture(0)
sound_playing = False

def get_label(handedness):
    return handedness.classification[0].label

while True:
    ret, image = cap.read()
    if not ret:
        break

    image = cv2.flip(image, 1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_image)

    if result.multi_hand_landmarks and result.multi_handedness:
        for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            label = get_label(handedness)
            lm = hand_landmarks.landmark

            # Gyan Mudra detection for LEFT hand
            if label == "Left":
                thumb_tip = lm[4]
                index_tip = lm[8]
                distance = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5

                # Threshold distance for thumb and index touching
                if distance < 0.05:
                    if not sound_playing:
                        pygame.mixer.music.play(-1)
                        sound_playing = True
                else:
                    if sound_playing:
                        pygame.mixer.music.stop()
                        sound_playing = False

            # Volume control for RIGHT hand
            if label == "Right":
                index_finger_y = lm[8].y
                volume = 1.0 - index_finger_y  # Y goes down as hand moves up
                volume = max(0.0, min(1.0, volume))
                pygame.mixer.music.set_volume(volume)
                cv2.putText(image, f'Volume: {int(volume*100)}%', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.imshow("Gyan Mudra Music Control", image)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()
