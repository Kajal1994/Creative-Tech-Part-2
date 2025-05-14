import cv2
import mediapipe as mp
import numpy as np
import random
import threading
import os
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load chakra images and backgrounds
sacral_img = cv2.imread("sacral.png", cv2.IMREAD_UNCHANGED)
root_img = cv2.imread("root.png", cv2.IMREAD_UNCHANGED)
bg_sacral = cv2.imread("BGEffect.jpg")
bg_root = cv2.imread("BGRoot.jpeg")

# Verify all files exist
required_files = [
    "sacral.png", "root.png",
    "BGEffect.jpg", "BGRoot.jpeg",
    "sacral.mp3", "Aum.mp3"
]

for file in required_files:
    if not os.path.exists(file):
        print(f"Error: {file} not found.")
        exit()

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Improved Sound Manager using pygame
class SoundManager:
    def __init__(self):
        self.current_sound = None
        
    def play(self, sound_file):
        if self.current_sound != sound_file:
            self.current_sound = sound_file
            try:
                pygame.mixer.music.load(sound_file)
                pygame.mixer.music.play(-1)  # -1 for infinite loop
            except Exception as e:
                print(f"Sound error: {e}")

    def stop(self):
        pygame.mixer.music.stop()

sound_manager = SoundManager()

# Chakra settings with corrected animations
chakras = {
    "sacral": {
        "gesture": lambda lm: np.linalg.norm([
            lm.landmark[4].x - lm.landmark[20].x,
            lm.landmark[4].y - lm.landmark[20].y
        ]) < 0.07,
        "image": sacral_img,
        "sound": "sacral.mp3",
        "background": bg_sacral,
        "color": (0, 215, 255)  # Orange
    },
    "root": {
        "gesture": lambda lm: np.linalg.norm([
            lm.landmark[4].x - lm.landmark[8].x,
            lm.landmark[4].y - lm.landmark[8].y
        ]) < 0.07,
        "image": root_img,
        "sound": "Aum.mp3",
        "background": bg_root,
        "color": (0, 0, 255)  # Red
    }
}

class ZoomImage:
    def __init__(self, x, y, base_img):
        self.x, self.y = x, y
        self.size = 50
        self.base_img = base_img
        self.target_size = 130
        self.speed = 1
        self.direction = 1  # 1=zoom in, -1=zoom out

    def update(self):
        self.size += self.speed * self.direction
        if self.size >= self.target_size or self.size <= 50:
            self.direction *= -1  # Reverse direction

    def draw(self, frame):
        try:
            img = cv2.resize(self.base_img, (self.size, self.size))
            y_end = self.y + img.shape[0]
            x_end = self.x + img.shape[1]
            
            if y_end > frame.shape[0] or x_end > frame.shape[1]:
                return
                
            for c in range(3):
                frame[self.y:y_end, self.x:x_end, c] = \
                    img[:, :, c] * (img[:, :, 3]/255.0) + \
                    frame[self.y:y_end, self.x:x_end, c] * (1.0 - img[:, :, 3]/255.0)
        except Exception as e:
            print(f"Drawing error: {e}")

class Glitter:
    def __init__(self, w, h, color):
        self.x = random.randint(0, w)
        self.y = random.randint(0, h)
        self.color = color
        self.dy = random.uniform(-0.5, 0.5)

    def update(self):
        self.y += self.dy
        if self.y < 0 or self.y > 480:
            self.y = random.randint(0, 480)
            self.x = random.randint(0, 640)
    
    def draw(self, frame):
        try:
            cv2.circle(frame, (int(self.x), int(self.y)), 3, self.color, -1)
        except Exception as e:
            print(f"Glitter error: {e}")

# Main loop
current_chakra = None
image_objects = []
glitter_particles = []

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    h, w = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    
    detected_chakra = None
    current_gestures = []
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Check for all possible gestures
            for name, chakra in chakras.items():
                if chakra["gesture"](hand_landmarks):
                    current_gestures.append(name)
    
    # Select the last detected gesture (most recent)
    if current_gestures:
        detected_chakra = current_gestures[-1]

    # Update state only when detection changes
    if detected_chakra != current_chakra:
        sound_manager.stop()
        current_chakra = detected_chakra
        image_objects.clear()
        glitter_particles.clear()
        if current_chakra:
            print(f"Switching to: {current_chakra}")
            sound_manager.play(chakras[current_chakra]["sound"])
    
    # Visual effects
    if current_chakra:
        chakra = chakras[current_chakra]
        bg = cv2.resize(chakra["background"], (w, h))
        frame = cv2.addWeighted(bg, 0.5, frame, 0.5, 0)
        
        # Create zoom images
        if len(image_objects) < 15:
            x = random.randint(0, w-150)
            y = random.randint(0, h-150)
            image_objects.append(ZoomImage(x, y, chakra["image"]))
        
        # Create glitter particles
        if len(glitter_particles) < 50:
            glitter_particles.extend(Glitter(w, h, chakra["color"]) for _ in range(5))
        
        # Update and draw effects
        for obj in image_objects:
            obj.update()
            obj.draw(frame)
            
        for glitter in glitter_particles:
            glitter.update()
            glitter.draw(frame)
    
    cv2.imshow("Chakra System", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

sound_manager.stop()
cap.release()
cv2.destroyAllWindows()
