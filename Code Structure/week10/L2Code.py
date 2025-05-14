import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

chakra_names = ['Root', 'Sacral', 'Solar Plexus', 'Heart', 'Throat', 'Third Eye', 'Crown']

show_menu = False
selected_chakra = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    index_finger_tip = None

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x = int(index_finger_tip.x * w)
            y = int(index_finger_tip.y * h)

            cv2.circle(frame, (x, y), 10, (255, 0, 255), -1)

            # Check if finger touches the menu button
            if 10 < x < 200 and 50 < y < 80:
                show_menu = not show_menu
                selected_chakra = None

            # If menu is visible, check for chakra selection
            if show_menu:
                start_y = 140  # Push chakra list down to avoid overlapping with button
                for i, chakra in enumerate(chakra_names):
                    cy = start_y + i * 35
                    if 10 < x < 200 and cy - 10 < y < cy + 10:
                        selected_chakra = chakra

    # Draw the menu button
    cv2.rectangle(frame, (10, 50), (200, 80), (0, 128, 255), -1)
    cv2.putText(frame, "Chakra List", (20, 72), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Show chakra list if menu is on
    if show_menu:
        start_y = 140
        for i, chakra in enumerate(chakra_names):
            cy = start_y + i * 35
            cv2.putText(frame, chakra, (30, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Show selected chakra info in center
    if selected_chakra:
        text = f"This is {selected_chakra} Chakra"
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 2)[0]
        text_x = int((w - text_size[0]) / 2)
        text_y = 400
        cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

    cv2.imshow("Chakra Touch Menu", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()
