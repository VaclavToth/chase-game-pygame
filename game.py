import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 1200
window_height = 800
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Chase Game")

# Set up the game clock
clock = pygame.time.Clock()

# Set up timing variables
obstacle_generation_interval = 10  # in seconds
last_obstacle_generation_time = time.time()

# Set up the characters
character_size = 50
player_x = (window_width - character_size) // 2
player_y = (window_height - character_size) // 2
chaser_x = random.randint(0, window_width - character_size)
chaser_y = random.randint(0, window_height - character_size)
character_speed = 5
chaser_speed = character_speed / 2
chaser_jump_distance = window_width // 3
chaser_jump_cooldown = 3000  # milliseconds
chaser_last_jump_time = pygame.time.get_ticks() - chaser_jump_cooldown

# Set up game state
is_chaser = True
game_over = False

# Obstacle properties
obstacle_width = 40
obstacle_height = 40
obstacle_color = (0, 0, 255)
obstacle_x = 200
obstacle_y = 300

# List to store obstacles
obstacles = []

# Set up scoring
score = 0
font = pygame.font.Font(None, 36)

# Helper function to restart the game
def restart_game():
    global player_x, player_y, chaser_x, chaser_y, game_over, score
    score = 0
    player_x = (window_width - character_size) // 2
    player_y = (window_height - character_size) // 2
    chaser_x = random.randint(0, window_width - character_size)
    chaser_y = random.randint(0, window_height - character_size)
    game_over = False
    # Clear the obstacles
    obstacles.clear()

def generate_obstacle():
    obstacle_x = random.randint(0, window_width - character_size)
    obstacle_y = random.randint(0, window_height - character_size)
    obstacles.append((obstacle_x, obstacle_y))

# Helper function to handle chaser jumping
def chaser_jump():
    global chaser_x, chaser_y, chaser_last_jump_time
    current_time = pygame.time.get_ticks()
    if current_time - chaser_last_jump_time > chaser_jump_cooldown:
        chaser_last_jump_time = current_time
        if abs(player_x - chaser_x) > abs(player_y - chaser_y):
            if player_x < chaser_x:
                chaser_x -= chaser_jump_distance
            elif player_x > chaser_x:
                chaser_x += chaser_jump_distance
        else:
            if player_y < chaser_y:
                chaser_y -= chaser_jump_distance
            elif player_y > chaser_y:
                chaser_y += chaser_jump_distance

# Game loop
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                restart_game()

    if not game_over:
        
        # Update the score
        score += 1

        # Get the state of the WSAD keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_x -= character_speed
        if keys[pygame.K_d]:
            player_x += character_speed
        if keys[pygame.K_w]:
            player_y -= character_speed
        if keys[pygame.K_s]:
            player_y += character_speed
        
        current_time = time.time()
        if current_time - last_obstacle_generation_time >= obstacle_generation_interval:
            generate_obstacle()
            last_obstacle_generation_time = current_time


        # Update the game state
        if is_chaser:
            current_time = pygame.time.get_ticks()

            # Automatically make the chaser jump
            if current_time - chaser_last_jump_time > chaser_jump_cooldown:
                chaser_jump()
                chaser_last_jump_time = current_time

            # Move the chaser towards the player
            if player_x < chaser_x:
                chaser_x -= chaser_speed
            elif player_x > chaser_x:
                chaser_x += chaser_speed
            if player_y < chaser_y:
                chaser_y -= chaser_speed
            elif player_y > chaser_y:
                chaser_y += chaser_speed

            # Check for collision between player and chaser
            if (
                player_x < chaser_x + character_size
                and player_x + character_size > chaser_x
                and player_y < chaser_y + character_size
                and player_y + character_size > chaser_y
            ):
                game_over = True
            
            # Check collision with obstacles
            for obstacle in obstacles:
                obstacle_x, obstacle_y = obstacle
                if player_x < obstacle_x + obstacle_width and \
                player_x + character_size > obstacle_x and \
                player_y < obstacle_y + obstacle_height and \
                player_y + character_size > obstacle_y:
                    # Collision occurred
                    print("Player collided with an obstacle!")
                    game_over = True

        # Keep the characters within the game window
        player_x = max(0, min(player_x, window_width - character_size))
        player_y = max(0, min(player_y, window_height - character_size))
        chaser_x = max(0, min(chaser_x, window_width - character_size))
        chaser_y = max(0, min(chaser_y, window_height - character_size))

    # Render the game
    window.fill((0, 0, 0))  # Clear the window

    # Draw the player dummy
    pygame.draw.rect(window, (255, 0, 0), (player_x, player_y + character_size // 2, character_size, character_size // 2))  # Body
    pygame.draw.circle(window, (255, 0, 0), (player_x + character_size // 2, player_y + character_size // 4), character_size // 4)  # Head

    # Draw the chaser dummy
    pygame.draw.rect(window, (0, 255, 0), (chaser_x, chaser_y + character_size // 2, character_size, character_size // 2))  # Body
    pygame.draw.circle(window, (0, 255, 0), (chaser_x + character_size // 2, chaser_y + character_size // 4), character_size // 4)  # Head

    # Draw the obstacle
    for obstacle in obstacles:
        obstacle_x, obstacle_y = obstacle
        pygame.draw.rect(window, obstacle_color, (obstacle_x, obstacle_y, obstacle_width, obstacle_height))

    # Draw the score
    score_text = font.render("Score: " + str(score), True, "BLUE")
    window.blit(score_text, (10, 10))

    # Draw game over message and restart instructions
    if game_over:
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over! Press 'R' to restart.", True, (255, 255, 255))
        text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
        window.blit(text, text_rect)

    pygame.display.flip()  # Update the window

    # Limit the frame rate
    clock.tick(60)

# Clean up Pygame
pygame.quit()