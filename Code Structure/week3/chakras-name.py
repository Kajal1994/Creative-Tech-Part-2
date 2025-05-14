chakras = [
    ("Root", "Base of Spine", "\033[91m"),  # Red
    ("Sacral", "Below Navel", "\033[33m"),  # Orange
    ("Solar Plexus", "Above Navel", "\033[93m"),  # Yellow
    ("Heart", "Center of Chest", "\033[92m"),  # Green
    ("Throat", "Throat Area", "\033[94m"),  # Blue
    ("Third Eye", "Between Eyebrows", "\033[95m"),  # Indigo
    ("Crown", "Top of Head", "\033[97m")  # Violet
]

reset_color = "\033[0m"  # Reset color after printing

# Printing chakras with colors and positions
print("The 7 Chakras, Their Positions, and Colors:")
for name, position, color in chakras:
    print(f"{color}- {name} Chakra ({position}){reset_color}")