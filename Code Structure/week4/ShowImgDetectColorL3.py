import cv2
import numpy as np

# Load chakra image
chakra_image = cv2.imread("demo.png")  # Replace with actual chakra image file
chakra_image = cv2.resize(chakra_image, (150, 150))  # Resize chakra image as needed

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define color range for red detection (Adjust as needed)
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # Create masks for red detection
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2  # Combine both red color masks

    # If red color is detected, overlay the chakra image
    if cv2.countNonZero(mask) > 500:  # Threshold to avoid noise
        x_offset, y_offset = 50, 50  # Position of chakra image
        x_end, y_end = x_offset + chakra_image.shape[1], y_offset + chakra_image.shape[0]

        # Create a region of interest (ROI)
        roi = frame[y_offset:y_end, x_offset:x_end]

        # Convert chakra image to same format as frame
        chakra_gray = cv2.cvtColor(chakra_image, cv2.COLOR_BGR2GRAY)
        _, mask_inv = cv2.threshold(chakra_gray, 1, 255, cv2.THRESH_BINARY)

        # Mask the region where the chakra image will be placed
        bg = cv2.bitwise_and(roi, roi, mask=cv2.bitwise_not(mask_inv))
        fg = cv2.bitwise_and(chakra_image, chakra_image, mask=mask_inv)

        # Combine background and foreground
        frame[y_offset:y_end, x_offset:x_end] = cv2.add(bg, fg)

    # Show the video feed
    cv2.imshow("Chakra Detection", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
