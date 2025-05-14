import cv2
import mediapipe as mp
import numpy as np
import random
from playsound import playsound
import threading

# Load chakra overlay image (transparent PNG)
chakra_img = cv2.imread("sacral.png", cv2.IMREAD_UNCHANGED)
base_chakra = cv2.resize(chakra_img, (150, 150))

# Load chakra background image
bg_image = cv2.imread("BGEffect.jpg")

# MediaPipe for hand detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

gesture_detected = False
image_objects = []
glitter_particles = []
sound_played = False

# Sparkle color (golden tone in BGR)
sparkle_color = (0, 215, 255)

class ZoomImage:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.size = random.randint(30, 60)
        self.scale_direction = 1
        self.max_size = 130
        self.min_size = 50

    def update(self):
        if self.scale_direction == 1:
            self.size += 2
            if self.size >= self.max_size:
                self.scale_direction = -1
        else:
            self.size -= 2
            if self.size <= self.min_size:
                self.scale_direction = 1

    def draw(self, frame):
        img = cv2.resize(base_chakra, (self.size, self.size))
        for c in range(3):
            frame[self.y:self.y+img.shape[0], self.x:self.x+img.shape[1], c] = \
                img[:, :, c] * (img[:, :, 3] / 255.0) + \
                frame[self.y:self.y+img.shape[0], self.x:self.x+img.shape[1], c] * (1.0 - img[:, :, 3] / 255.0)

class Glitter:
    def __init__(self, w, h):
        self.x = random.randint(0, w)
        self.y = random.randint(0, h)
        self.radius = random.randint(2, 5)
        self.color = sparkle_color
        self.opacity = random.uniform(0.4, 1.0)
        self.dy = random.uniform(-1.2, 1.2)

    def update(self):
        self.y += self.dy
        if self.y < 0 or self.y > 480:
            self.y = random.randint(0, 480)
            self.x = random.randint(0, 640)

    def draw(self, frame):
        overlay = frame.copy()
        cv2.circle(overlay, (int(self.x), int(self.y)), self.radius, self.color, -1)
        cv2.addWeighted(overlay, self.opacity, frame, 1 - self.opacity, 0, frame)

# ✅ Modified gesture: Thumb tip touching Pinky tip
def detect_custom_gesture(hand_landmarks):
    # Thumb tip (4), Pinky tip (20)
    thumb_tip = hand_landmarks.landmark[4]
    pinky_tip = hand_landmarks.landmark[20]
    
    # Distance between thumb and pinky tip
    distance = np.sqrt((thumb_tip.x - pinky_tip.x)**2 + (thumb_tip.y - pinky_tip.y)**2)

    return distance < 0.05  # You can try 0.06 or 0.07 if needed

def play_sound_once():
    global sound_played
    if not sound_played:
        threading.Thread(target=playsound, args=("sacral.mp3",), daemon=True).start()
        sound_played = True

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Resize background image to match camera feed
    bg = cv2.resize(bg_image, (w, h))

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    gesture_detected = False

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            if detect_custom_gesture(hand_landmarks):
                gesture_detected = True
                play_sound_once()
            else:
                sound_played = False

    if gesture_detected:
        frame = cv2.addWeighted(bg, 0.5, frame, 0.5, 0)

        if len(image_objects) < 30:
            attempts = 0
            while len(image_objects) < 30 and attempts < 300:
                x = random.randint(0, w - 150)
                y = random.randint(0, h - 150)
                too_close = False
                for obj in image_objects:
                    distance = np.sqrt((obj.x - x) ** 2 + (obj.y - y) ** 2)
                    if distance < 120:
                        too_close = True
                        break
                if not too_close:
                    image_objects.append(ZoomImage(x, y))
                attempts += 1

        if len(glitter_particles) < 100:
            for _ in range(5):
                glitter_particles.append(Glitter(w, h))
    else:
        image_objects.clear()
        glitter_particles.clear()

    for obj in image_objects:
        obj.update()
        obj.draw(frame)

    for glitter in glitter_particles:
        glitter.update()
        glitter.draw(frame)

    cv2.imshow("Chakra Background & Effects", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
