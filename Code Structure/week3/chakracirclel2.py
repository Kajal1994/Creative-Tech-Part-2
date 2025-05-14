import pygame
# Initialize Pygame
pygame.init()
# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chakra Visualisation")

# Chakra colors (RGB format)
chakra_colors = [
    (255, 0, 0),    # Root - Red
    (255, 165, 0),  # Sacral - Orange
    (255, 255, 0),  # Solar Plexus - Yellow
    (0, 128, 0),    # Heart - Green
    (0, 0, 255),    # Throat - Blue
    (75, 0, 130),   # Third Eye - Indigo
    (238, 130, 238) # Crown - Violet
]

# Chakra positions
chakra_positions = [
     (WIDTH // 2, HEIGHT - 50),   # Root Chakra
    (WIDTH // 2, HEIGHT - 120),  # Sacral Chakra
    (WIDTH // 2, HEIGHT - 190),  # Solar Plexus Chakra
    (WIDTH // 2, HEIGHT - 260),  # Heart Chakra
    (WIDTH // 2, HEIGHT - 330),  # Throat Chakra
    (WIDTH // 2, HEIGHT - 400),  # Third Eye Chakra
    (WIDTH // 2, HEIGHT - 470)   # Crown Chakra
]
# Main loop
running = True
while running:
    screen.fill((0, 0, 0))  # Black background
    # Draw chakra circles
    for i in range(7):
        pygame.draw.circle(screen, chakra_colors[i], chakra_positions[i], 30)  # Draw circles

    pygame.display.flip()  # Update display

    # Event loop to close window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
# Quit Pygame
pygame.quit()
