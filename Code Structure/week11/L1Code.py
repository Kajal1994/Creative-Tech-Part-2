import cv2
import mediapipe as mp
import numpy as np
import random

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

chakra_colors = {
    'Root': (0, 0, 255),         # Red
    'Sacral': (0, 165, 255),     # Orange
    'Solar Plexus': (0, 255, 255), # Yellow
    'Heart': (0, 255, 0),        # Green
    'Throat': (255, 0, 0),       # Blue
    'Third Eye': (130, 0, 75),   # Indigo
    'Crown': (255, 255, 0)       # Violet
}

chakra_names = list(chakra_colors.keys())
show_menu = False
selected_chakra = None
particles = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Hand detection
    result = hands.process(rgb_frame)
    index_finger_tip = None
    
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x = int(index_finger_tip.x * w)
            y = int(index_finger_tip.y * h)
            cv2.circle(frame, (x, y), 10, (255, 0, 255), -1)

    # Menu interaction
    if index_finger_tip:
        ix, iy = int(index_finger_tip.x * w), int(index_finger_tip.y * h)
        
        if 10 < ix < 200 and 50 < iy < 80:
            show_menu = not show_menu
            selected_chakra = None
        
        if show_menu:
            start_y = 140
            for i, chakra in enumerate(chakra_names):
                cy = start_y + i * 35
                if 10 < ix < 200 and cy-10 < iy < cy+10:
                    selected_chakra = chakra
                    # Reset particles on new selection
                    particles = []

    # Generate new particles
    if selected_chakra:
        # Add 10 new particles per frame at random positions
        for _ in range(10):
            particles.append({
                'x': random.randint(0, w),
                'y': random.randint(0, h),
                'color': chakra_colors[selected_chakra]
            })

    # Update and draw particles
    for particle in particles[:]:
        # Move particles upward
        particle['y'] -= 1
        if particle['y'] < 0:
            particles.remove(particle)
        else:
            cv2.circle(frame, (particle['x'], particle['y']), 
                      3, particle['color'], -1)

    # Draw UI elements
    cv2.rectangle(frame, (10, 50), (200, 80), (0, 128, 255), -1)
    cv2.putText(frame, "Chakra List", (20, 72), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    if show_menu:
        start_y = 140
        for i, chakra in enumerate(chakra_names):
            cy = start_y + i * 35
            cv2.putText(frame, chakra, (30, cy), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Chakra Touch Menu", frame)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
