import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Initialize the mixer for sound
pygame.mixer.init()

# Create screen
screen = pygame.display.set_mode((800, 600))

# Background image
background = pygame.image.load('images/bgimg1.jpg')

# Background music
pygame.mixer.music.load('sounds/game-over-2-sound-effect-230463.mp3')  # Load your background music file
pygame.mixer.music.play(-1)  # Play background music indefinitely

# Sound effects
bullet_sound = pygame.mixer.Sound('sounds/single-gunshot-54-40780.mp3')  # Sound when bullet is fired
collision_sound = pygame.mixer.Sound('sounds/alien-intruder-210485.mp3')  # Sound when enemy is hit

# Title and icon
pygame.display.set_caption("Space Invasion")
icon = pygame.image.load('images/galaxy (1).png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('images/astronaut (2).png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = pygame.image.load('images/devil.png')
num_of_enemies = 6  # Number of enemies

# Lists for multiple enemies
enemyImg_list = []
enemyX_list = []
enemyY_list = []
enemyX_change_list = []
enemyY_change_list = []

for i in range(num_of_enemies):
    enemyImg_list.append(pygame.image.load('images/devil.png'))
    enemyX_list.append(random.randint(0, 736))  # Random X position
    enemyY_list.append(random.randint(50, 150))  # Random Y position
    enemyX_change_list.append(0.3)  # Movement speed in X
    enemyY_change_list.append(40)   # Movement speed in Y after hitting edge

# Bullet
bulletImg = pygame.image.load('images/food.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = "ready"  # "ready" means the bullet is not visible

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)  # Load a font

# Function to show score on the screen
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))  # White color
    screen.blit(score, (x, y))

# Function to draw player on the screen
def player(x, y):
    screen.blit(playerImg, (x, y))

# Function to draw enemy on the screen
def enemy(x, y, i):
    screen.blit(enemyImg_list[i], (x, y))

# Function to fire the bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))
    bullet_sound.play()  # Play bullet firing sound

# Function to detect collision between bullet and enemy
def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    return distance < 27  # Adjust collision radius as necessary
# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Function to show game over text
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))  # White color
    screen.blit(over_text, (200, 250))  # Centered on the screen

# Game loop
running = True
game_over = False  # To track whether the game is over
while running:
    # Fill the screen with black and draw background
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for key presses
        if event.type == pygame.KEYDOWN:
            if not game_over:  # Prevent movement if game is over
                if event.key == pygame.K_LEFT:
                    playerX_change = -4  # Move left
                if event.key == pygame.K_RIGHT:
                    playerX_change = +4  # Move right
                if event.key == pygame.K_SPACE and bullet_state == "ready":
                    bulletX = playerX  # Get the current X coordinate of the player
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0  # Stop moving when key is released

    # Update player position
    playerX += playerX_change

    # Prevent player from going out of bounds
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736  # 800 - width of player (assuming 64px wide player)

    # Update and draw each enemy
    for i in range(num_of_enemies):
        if enemyY_list[i] > 440:  # Game over if any enemy goes below this line
            for j in range(num_of_enemies):
                enemyY_list[j] = 2000  # Move enemies off the screen
            game_over = True  # Set game over flag to True
            game_over_text()  # Display "Game Over" text
            break

        enemyX_list[i] += enemyX_change_list[i]

        # Reverse direction when hitting screen edges and move down
        if enemyX_list[i] <= 0:
            enemyX_change_list[i] = 0.3  # Move right
            enemyY_list[i] += enemyY_change_list[i]  # Move down when it hits the edge
        elif enemyX_list[i] >= 736:
            enemyX_change_list[i] = -0.3  # Move left
            enemyY_list[i] += enemyY_change_list[i]  # Move down when it hits the edge

        # Check for collision between bullet and enemy
        collision = is_collision(enemyX_list[i], enemyY_list[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            enemyX_list[i] = random.randint(0, 736)  # Respawn enemy at random X position
            enemyY_list[i] = random.randint(50, 150)  # Respawn enemy at random Y position
            # Increment the score when an enemy is hit
            score_value += 1
            collision_sound.play()  # Play collision sound

        # Draw the enemy
        enemy(enemyX_list[i], enemyY_list[i], i)

    if not game_over:  # Prevent updates if game is over
        # Bullet movement
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        # Check if the bullet has gone off the screen
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        # Draw the player
        player(playerX, playerY)

        # Show the score
        show_score(10, 10)  # Position the score at the top left corner (x=10, y=10)

    # Update display
    pygame.display.update()

# Game loop
running = True
while running:
    # Fill the screen with black and draw background
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4  # Move left
            if event.key == pygame.K_RIGHT:
                playerX_change = +4 # Move right
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX  # Get the current X coordinate of the player
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0  # Stop moving when key is released

    # Update player position
    playerX += playerX_change

    # Prevent player from going out of bounds
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736  # 800 - width of player (assuming 64px wide player)

    # Update and draw each enemy
    for i in range(num_of_enemies):
        enemyX_list[i] += enemyX_change_list[i]

        # Reverse direction when hitting screen edges and move down
        if enemyX_list[i] <= 0:
            enemyX_change_list[i] = 0.3  # Move right
            enemyY_list[i] += enemyY_change_list[i]  # Move down when it hits the edge
        elif enemyX_list[i] >= 736:
            enemyX_change_list[i] = -0.3  # Move left
            enemyY_list[i] += enemyY_change_list[i]  # Move down when it hits the edge

        # Check for collision between bullet and enemy
        collision = is_collision(enemyX_list[i], enemyY_list[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            enemyX_list[i] = random.randint(0, 736)  # Respawn enemy at random X position
            enemyY_list[i] = random.randint(50, 150)  # Respawn enemy at random Y position
            # Increment the score when an enemy is hit
            score_value += 1
            collision_sound.play()  # Play collision sound

        # Draw the enemy
        enemy(enemyX_list[i], enemyY_list[i], i)

    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Check if the bullet has gone off the screen
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    # Draw the player
    player(playerX, playerY)

    # Show the score
    show_score(10, 10)  # Position the score at the top left corner (x=10, y=10)

    # Update display
    pygame.display.update()
