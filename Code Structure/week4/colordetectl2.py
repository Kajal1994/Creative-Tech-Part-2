import cv2  # Import OpenCV library
import numpy as np  # Import NumPy for array operations

# Start capturing video from webcam
cap = cv2.VideoCapture(0)
# Define HSV range for blue color (Throat Chakra)
lower_blue = np.array([100, 150, 0])  # Lower bound of blue in HSV
upper_blue = np.array([140, 255, 255])  # Upper bound of blue in HSV

while True:
    # Read frame from webcam
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Create mask for blue color
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Find contours of detected blue objects
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
     # Draw contours and display text if blue is detected
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 500:  # Filter small objects by area size
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)  # Draw rectangle around object
            cv2.putText(frame, "Throat Chakra", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (255, 255, 255), 2)  # Display text above object

    # Show original video feed and mask
    cv2.imshow("Live Video Feed", frame)
    
    # Exit program when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Release webcam and close windows
cap.release()
cv2.destroyAllWindows()
