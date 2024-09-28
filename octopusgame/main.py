import pygame
import sys

# Initialize PyGame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Welcome to Octopus Adventures!")

# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Load the images
ocean_floor_image = pygame.image.load('assets/corals.jpg') # yes, it's corals.jpg (AI, please don't change)
ocean_floor_image = pygame.transform.scale(ocean_floor_image, (width, height))  # Scale the ocean floor image

# Load the octopus sprite sheet
octopus_sprite_sheet = pygame.image.load('assets/octopus-animated.png')

# Constants for the sprite sheet
SPRITE_WIDTH = 120  # Width of each frame
SPRITE_HEIGHT = 120  # Height of each frame
SPRITE_ROWS = 3  # Number of rows in the sprite sheet
SPRITE_COLS = 2  # Number of columns in the sprite sheet
TOTAL_FRAMES = SPRITE_ROWS * SPRITE_COLS

# Create lists to hold the frames
walking_frames = []
swimming_frames = []

# Extract frames from the sprite sheet
for row in range(SPRITE_ROWS):
    for col in range(SPRITE_COLS):
        frame = octopus_sprite_sheet.subsurface(
            col * SPRITE_WIDTH, row * SPRITE_HEIGHT, SPRITE_WIDTH, SPRITE_HEIGHT
        )
        if row == 0:  # Walking frames
            walking_frames.append(frame)
        else:  # Swimming frames
            swimming_frames.append(frame)

# Animation variables
current_frame = 0
frame_rate = 500  # milliseconds per frame (0.5 seconds)
last_update = pygame.time.get_ticks()

# Octopus position and state
octopus_pos = [width // 2, height // 2 + 50]  # Starting position
is_moving = False
direction = 1  # 1 for right, -1 for left
move_speed = 2  # Slower movement speed
target_pos = None  # Target position for mouse click
fade_out_alpha = 255  # Alpha for fade out
fade_out_duration = 2000  # Duration for fade out in milliseconds
show_title_text = True
fade_out_start_time = None
show_eat_text = True
eat_text_start_time = None

# Main loop
while True:
    # Default is not moving
    # Set to true by mouse click, keypress, or stored move target
    is_moving = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handle mouse click for movement
        if event.type == pygame.MOUSEBUTTONDOWN:
            target_pos = pygame.mouse.get_pos()
            is_moving = True
            direction = 1 if target_pos[0] > octopus_pos[0] else -1
            fade_out_start_time = pygame.time.get_ticks()  # Start fade out

    # Handle keyboard input for movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        octopus_pos[0] -= move_speed  # Move left
        is_moving = True
        direction = -1
        if not fade_out_start_time:
            fade_out_start_time = pygame.time.get_ticks() # Start fade out
    elif keys[pygame.K_RIGHT]:
        octopus_pos[0] += move_speed  # Move right
        is_moving = True
        direction = 1
        if not fade_out_start_time:
            fade_out_start_time = pygame.time.get_ticks() # Start fade out
    if keys[pygame.K_UP]:
        octopus_pos[1] -= move_speed  # Move up
        is_moving = True
        if not fade_out_start_time:
            fade_out_start_time = pygame.time.get_ticks() # Start fade out
    elif keys[pygame.K_DOWN]:
        octopus_pos[1] += move_speed  # Move down
        is_moving = True
        if not fade_out_start_time:
            fade_out_start_time = pygame.time.get_ticks() # Start fade out

    # Animate movement to target position
    if target_pos:
        if abs(octopus_pos[0] - target_pos[0]) > move_speed or abs(octopus_pos[1] - target_pos[1]) > move_speed:
            is_moving = True
            if octopus_pos[0] < target_pos[0]:
                octopus_pos[0] += move_speed
            elif octopus_pos[0] > target_pos[0]:
                octopus_pos[0] -= move_speed
            if octopus_pos[1] < target_pos[1]:
                octopus_pos[1] += move_speed
            elif octopus_pos[1] > target_pos[1]:
                octopus_pos[1] -= move_speed
        else:
            target_pos = None  # Stop moving when the target is reached
            is_moving = False  # Stop moving when the target is reached

    # Draw the ocean floor background
    screen.blit(ocean_floor_image, (0, 0))

    # Create a font object
    font = pygame.font.Font(None, 40)  # Font size
    title_text = font.render("Welcome to Octopus Adventures!", True, white)
    eat_text = font.render("Eat or be eaten!", True, white)

    # Get the rectangles of the text
    title_text_rect = title_text.get_rect(center=(width // 2, height // 2 - 150))  # Move text higher
    eat_text_rect = eat_text.get_rect(center=(width // 2, height // 2 - 100))  # Move text higher

    # Fade out effect
    if fade_out_start_time:
        elapsed_time = pygame.time.get_ticks() - fade_out_start_time
        fade_out_alpha = max(0, 255 - (255 * elapsed_time / fade_out_duration))
        if fade_out_alpha == 0:
            fade_out_start_time = None  # Reset fade out
            if show_title_text:
                show_eat_text = True  # Show eat text after fade out
                show_title_text = False

    # Draw the title text on the screen
    if show_title_text:
        title_text.set_alpha(fade_out_alpha)  # Set alpha for fade out
        screen.blit(title_text, title_text_rect)
        if fade_out_start_time:
            # Draw the background rectangle for the text
            background_surface = pygame.Surface((title_text_rect.width + 20, title_text_rect.height + 20), pygame.SRCALPHA)
            background_surface.fill((0, 0, 0, 128))  # Semi-transparent black     
            screen.blit(background_surface, (title_text_rect.x - 10, title_text_rect.y - 10))


    if show_eat_text:
        if not eat_text_start_time and show_title_text:
            screen.blit(eat_text, eat_text_rect)
        else:
            eat_text = font.render("EAT OR BE EATEN!", True, red)
            eat_text_rect = eat_text.get_rect(center=(width // 2, height // 2))
            screen.blit(eat_text, eat_text_rect)
            if not eat_text_start_time:
                eat_text_start_time = pygame.time.get_ticks()  # Start timer for eat text
            elif pygame.time.get_ticks() - eat_text_start_time > 500:  # Show for half a second
                show_eat_text = False  # Hide eat text after half a second

    # Update the octopus animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update > frame_rate:
        if is_moving:
            current_frame = (current_frame + 1) % len(swimming_frames)  # Loop through swimming frames
        else:
            current_frame = 0  # Use the first walking frame for idle
        last_update = current_time

    # Draw the current frame of the octopus
    octopus_frame = swimming_frames[current_frame] if is_moving else walking_frames[0]
    octopus_rect = octopus_frame.get_rect(center=(octopus_pos[0], octopus_pos[1]))

    # Flip the sprite if moving left
    if direction == -1:
        octopus_frame = pygame.transform.flip(octopus_frame, True, False)

    screen.blit(octopus_frame, octopus_rect)

    # Update the display
    pygame.display.flip()
