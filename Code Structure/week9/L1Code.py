import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()

print("Say something...")

try:
    # Use the microphone as the source of input
    with sr.Microphone() as source:
        print("Adjusting for background noise...")
        recognizer.adjust_for_ambient_noise(source)  # Reduce noise
        print("Listening...")
        audio = recognizer.listen(source)  # Capture audio input

    # Recognize speech using Google Web Speech API
    print("Recognizing...")
    text = recognizer.recognize_google(audio)  # Convert audio to text
    print(f"You said: {text}")

except sr.UnknownValueError:
    print("Sorry, I couldn’t understand what you said.")
except sr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")
except Exception as e:
    print(f"An error occurred: {e}")
