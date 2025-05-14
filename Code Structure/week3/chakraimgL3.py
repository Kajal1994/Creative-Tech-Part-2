import cv2
import numpy as np

# Set fixed output window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Chakra details
chakra_name = "Sacral Chakra"
chakra_image = "demo.png"  # Ensure the image is in the same folder as the script

# Load the image
img = cv2.imread(chakra_image)

if img is None:
    print(f"Error: Image '{chakra_image}' not found! Ensure it is in the same folder as this script.")
else:
    # Resize image while maintaining aspect ratio
    img_height, img_width = img.shape[:2]
    scale = min(WINDOW_WIDTH / img_width, WINDOW_HEIGHT / img_height) * 0.8  # Scale down to fit inside the window
    new_width = int(img_width * scale)
    new_height = int(img_height * scale)
    img_resized = cv2.resize(img, (new_width, new_height))

    # Create a blank canvas (black background) with fixed window size
    canvas = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)

    # Calculate position to center the image
    x_offset = (WINDOW_WIDTH - new_width) // 2
    y_offset = (WINDOW_HEIGHT - new_height) // 2

    # Place the resized image onto the canvas
    canvas[y_offset:y_offset+new_height, x_offset:x_offset+new_width] = img_resized

    # Add chakra name text on the canvas
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(canvas, chakra_name, (50, 550), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the fixed-size window
    cv2.imshow("Sacral Chakra", canvas)

    # Wait indefinitely until user presses 'q'
    while True:
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

# Close the OpenCV window
cv2.destroyAllWindows()
