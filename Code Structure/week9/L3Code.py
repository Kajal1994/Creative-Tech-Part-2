import speech_recognition as sr
import pygame
import os

# Initialize pygame mixer
pygame.mixer.init()

# Function to play root chakra sound
def play_root_sound():
    sound_file = "Aum.mp3"  # Ensure this file exists in the same directory
    if os.path.exists(sound_file):  # Check if the sound file exists
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.set_volume(1.0)  # Set volume to maximum
        pygame.mixer.music.play()
        print("Playing Root Chakra Sound...")
    else:
        print(f"Sound file '{sound_file}' not found!")

# Function to stop playing sound
def stop_sound():
    if pygame.mixer.music.get_busy():  # Check if music is currently playing
        pygame.mixer.music.stop()
        print("Stopped playing sound.")
    else:
        print("No sound is currently playing.")

# Set up speech recognizer
recognizer = sr.Recognizer()
print("Say 'I trust in the process of life' to play the Root Chakra sound or 'stop playing' to stop the sound...")

while True:  # Continuous listening loop
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        print("Listening...")

        try:
            audio = recognizer.listen(source)  # Capture audio input from microphone
            text = recognizer.recognize_google(audio)  # Convert speech to text using Google API
            print("You said:", text)

            # Check for specific phrases and trigger corresponding actions
            if "i trust in the process of life" in text.lower():
                play_root_sound()  # Play the corresponding sound when the phrase is correct
            elif "stop playing" in text.lower():
                stop_sound()  # Stop playing sound when the phrase is correct
            else:
                print("Command not recognized. Say 'I trust in the process of life.' or 'stop playing'.")

        except sr.UnknownValueError:
            print("Sorry, I couldn't understand.")
        except sr.RequestError:
            print("Could not connect to speech recognition service.")
