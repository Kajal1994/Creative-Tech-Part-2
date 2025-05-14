import cv2
import mediapipe as mp

# Chakra menu state
show_menu = False
chakra_names = ["Root", "Sacral", "Solar Plexus", "Heart", "Throat", "Third Eye", "Crown"]

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Function to check if index finger is touching button
def is_touching_button(index_x, index_y):
    return 20 <= index_x <= 170 and 20 <= index_y <= 60

# Start camera
cap = cv2.VideoCapture(0)
touched_last_frame = False  # to avoid repeat toggle

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process hand
    result = hands.process(rgb_frame)

    # Draw button
    cv2.rectangle(frame, (20, 20), (170, 60), (0, 100, 255), -1)
    cv2.putText(frame, "Chakra List", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            # Get index fingertip
            index_tip = handLms.landmark[8]
            index_x = int(index_tip.x * w)
            index_y = int(index_tip.y * h)

            # Draw circle on fingertip
            cv2.circle(frame, (index_x, index_y), 8, (255, 255, 0), -1)

            # Check if fingertip is touching the button
            if is_touching_button(index_x, index_y):
                if not touched_last_frame:
                    show_menu = not show_menu  # Toggle the menu
                    touched_last_frame = True
            else:
                touched_last_frame = False

    # Show chakra names if menu is open
    if show_menu:
        for i, chakra in enumerate(chakra_names):
            y = 80 + i * 30
            cv2.putText(frame, chakra, (30, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Chakra Touch Menu", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
