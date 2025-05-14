import cv2
import speech_recognition as sr

def show_root_chakra():
    img = cv2.imread("root.png")
    if img is not None:
        cv2.imshow("Root Chakra", img)
        cv2.waitKey(6000)  # Show image for 4 seconds
        cv2.destroyAllWindows()
    else:
        print("Image file not found or couldn't be loaded.")

# Set up the speech recognizer
recognizer = sr.Recognizer()

print("Say 'i trust myself and the journey of life' to show the Root Chakra image...")

with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source)
    print("Listening...")

    try:
        audio = recognizer.listen(source)
        spoken_text = recognizer.recognize_google(audio)
        print(f"You said: {spoken_text}")

        if 'i trust myself and the journey of life' in spoken_text.lower():
            show_root_chakra()
        else:
            print("That's not the root chakra.")

    except sr.UnknownValueError:
        print("Sorry, I didn't understand what you said.")
    except sr.RequestError:
        print("Could not request results from the speech service.")
