import cv2
import mediapipe as mp
import numpy as np
import threading
import os
from pygame import mixer
import random

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize pygame mixer for sound
mixer.init()

# Load background image
forest_path = "forest.jpg"
if os.path.exists(forest_path):
    forest_bg = cv2.imread(forest_path)
    forest_bg = cv2.resize(forest_bg, (640, 480))
else:
    forest_bg = np.zeros((480, 640, 3), dtype=np.uint8)

# Load sounds
aum_path = "Aum.mp3"
birds_path = "birds.mp3"
aum_loaded = os.path.exists(aum_path)
birds_loaded = os.path.exists(birds_path)

if aum_loaded:
    aum_sound = mixer.Sound(aum_path)
    aum_channel = mixer.Channel(1)
else:
    aum_channel = None

if birds_loaded:
    birds_sound = mixer.Sound(birds_path)

sound_playing = False
birds_playing = False

def play_aum():
    global sound_playing
    if not sound_playing and aum_loaded and aum_channel:
        sound_playing = True
        aum_channel.play(aum_sound)

# Start webcam
cap = cv2.VideoCapture(0)

particles = []
max_particles = 50
hand_detected = False

while cap.isOpened():
    success, img = cap.read()
    if not success:
        break

    height, width, _ = img.shape
    img = cv2.flip(img, 1)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        chakra_display = cv2.addWeighted(img, 0.7, forest_bg, 0.3, 0)

        # Add random particles
        if len(particles) < max_particles:
            particles.append({
                'x': random.randint(0, width-1),
                'y': random.randint(0, height-1),
                'dx': random.randint(-2, 2),
                'dy': random.randint(-4, -1),
                'color': (0, random.randint(150, 255), random.randint(150, 255)),
                'life': 30
            })

        # Draw hand landmarks
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(chakra_display, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Play sounds only on first detection
        if not hand_detected:
            hand_detected = True
            threading.Thread(target=play_aum).start()
            if birds_loaded and not birds_playing:
                birds_sound.play(-1)  # Loop birds sound
                birds_playing = True

        # Update and draw particles
        for particle in particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 1
            cv2.circle(chakra_display, (particle['x'], particle['y']), 3, particle['color'], -1)
            if particle['life'] <= 0 or not (0 <= particle['x'] < width) or not (0 <= particle['y'] < height):
                particles.remove(particle)

        cv2.putText(chakra_display, "Chakra Activation", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        cv2.imshow("Chakra Activation", chakra_display)
    else:
        # No hand detected: show webcam, stop sounds, reset flag
        if hand_detected:
            hand_detected = False
            if birds_loaded and birds_playing:
                birds_sound.stop()
                birds_playing = False
            if aum_loaded and sound_playing and aum_channel:
                aum_channel.stop()
                sound_playing = False
        particles.clear()
        cv2.imshow("Chakra Activation", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
if birds_loaded and birds_playing:
    birds_sound.stop()
if aum_loaded and sound_playing and aum_channel:
    aum_channel.stop()
