import cv2
import mediapipe as mp
import numpy as np

# Initialize Mediapipe Hands module
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# OpenCV video capture
cap = cv2.VideoCapture(0)

# Variables to store the last detected shape and chakra name
triangle_detected = False
chakra_name = ""
path = []

# Button properties for "Clear Shape"
button_x, button_y, button_w, button_h = 10, 10, 150, 50

# Chakra name position (right side of the screen)
chakra_name_x, chakra_name_y = 400, 50

def is_triangle(contour):
    """Check if the given contour forms a triangle."""
    epsilon = 0.04 * cv2.arcLength(contour, True)  # Approximation accuracy
    approx = cv2.approxPolyDP(contour, epsilon, True)  # Approximate the contour
    return len(approx) == 3  # Check if it has exactly 3 vertices

def distance(point1, point2):
    """Calculate Euclidean distance between two points."""
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame for better user interaction
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # Draw the "Clear Shape" button
    cv2.rectangle(frame, (button_x, button_y), (button_x + button_w, button_y + button_h), (0, 255, 0), -1)
    cv2.putText(frame, 'Clear Shape', (button_x + 10, button_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get index finger tip position
            index_finger_tip = hand_landmarks.landmark[8]
            h, w, _ = frame.shape
            x, y = int(index_finger_tip.x * w), int(index_finger_tip.y * h)

            # Check if the finger touches the "Clear Shape" button
            if button_x < x < button_x + button_w and button_y < y < button_y + button_h:
                path.clear()  # Clear the path
                triangle_detected = False  # Reset triangle detection
                chakra_name = ""  # Clear chakra name

            # Append current index finger position to the path
            path.append((x, y))

            # Draw the path on the screen
            for i in range(1, len(path)):
                cv2.line(frame, path[i - 1], path[i], (0, 0, 255), 2)

            # Check if a triangle is formed and fully completed
            if len(path) > 30:  # Ensure enough points are drawn to form a shape
                contour = np.array(path, dtype=np.int32)
                if is_triangle(contour):
                    start_point = path[0]
                    end_point = path[-1]
                    if distance(start_point, end_point) < 20:  # Ensure starting and ending points are close enough
                        triangle_detected = True
                        chakra_name = "Root Chakra"

    # Display Chakra Name if a triangle is detected (right side of the screen)
    if triangle_detected:
        cv2.putText(frame, chakra_name, (chakra_name_x, chakra_name_y), cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1.0, color=(0, 0, 255), thickness=2)

    # Show video feed with updates
    cv2.imshow("Chakra Drawing", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
