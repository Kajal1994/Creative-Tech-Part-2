# Importing the playsound module
from playsound import playsound

# Importing os to check if the file exists
import os

# Provide the absolute path to your sound file (replace with your actual file path)
sound_path = r"D:\cerative-tech-part2\week7\A.wav"  # Use raw string (r"") for Windows paths

# Check if file exists before playing
if os.path.exists(sound_path):
    print("Playing sound...")
    try:
        playsound(sound_path)  # Play the sound file
        print("Sound finished playing.")
    except Exception as e:
        print("An error occurred while playing the sound:", e)
else:
    print("Sound file not found. Please check the file path.")
