# importing libraries
import pygame
import time
import random

snake_speed = 15

# Window size
window_x = 720
window_y = 480

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Initialising pygame
pygame.init()

# Initialise game window
pygame.display.set_caption('GeeksforGeeks Snakes')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

# defining snake default position
snake_position = [100, 50]

# defining first 4 blocks of snake body
snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]]

# List to hold multiple fruit positions and their colors
# Fruit format: [x, y, color, spawn_time]
fruit_positions = []
# Timer for fruit spawning
fruit_spawn_timer = 0
FRUIT_SPAWN_INTERVAL = 4 * 1000  # Spawn new fruit every 4 seconds
FRUIT_LIFETIME = 2 * 1000  # Fruit disappears after 2 seconds

# setting default snake direction towards right
direction = 'RIGHT'
change_to = direction

# initial score
score = 0

# displaying Score function
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)

# game over function
def game_over(message):
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render(message + ' Your Score is : ' + str(score), True, white)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x / 2, window_y / 4)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()

# Main Function
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    snake_body.insert(0, list(snake_position))

    # Check for collision with any fruit
    ate_fruit = False
    for fruit in list(fruit_positions):  # Use list() to iterate over a copy
        if snake_position[0] == fruit[0] and snake_position[1] == fruit[1]:
            ate_fruit = True
            fruit_positions.remove(fruit)
            
            # Check fruit color for game logic
            if fruit[2] == blue:
                score += 10
                # Snake grows, so we don't pop the tail
            elif fruit[2] == red:
                game_over("You ate a red fruit!")
            elif fruit[2] == white:
                game_over("You ate a white fruit!")
            break
            
    # If a blue fruit was not eaten, the snake's tail shrinks
    if not ate_fruit or (ate_fruit and fruit[2] != blue):
        snake_body.pop()

    # Fruit spawning logic
    current_time = pygame.time.get_ticks()
    if current_time - fruit_spawn_timer > FRUIT_SPAWN_INTERVAL:
        num_fruits_to_spawn = random.randint(2, 5) # Spawn 2 to 5 fruits at a time
        for _ in range(num_fruits_to_spawn):
            fruit_x = random.randrange(1, (window_x // 10)) * 10
            fruit_y = random.randrange(1, (window_y // 10)) * 10
            
            # Randomly choose fruit color
            fruit_color_choice = random.choice([blue, white, red])
            fruit_positions.append([fruit_x, fruit_y, fruit_color_choice, current_time])
        fruit_spawn_timer = current_time

    # Remove old fruits
    for fruit in list(fruit_positions):
        if current_time - fruit[3] > FRUIT_LIFETIME:
            fruit_positions.remove(fruit)

    game_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    
    # Draw all fruits
    for fruit in fruit_positions:
        pygame.draw.rect(game_window, fruit[2], pygame.Rect(fruit[0], fruit[1], 10, 10))

    if snake_position[0] < 0 or snake_position[0] > window_x - 10:
        game_over("You hit the wall!")
    if snake_position[1] < 0 or snake_position[1] > window_y - 10:
        game_over("You hit the wall!")

    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over("You hit yourself!")

    show_score(1, white, 'times new roman', 20)
    pygame.display.update()
    fps.tick(snake_speed)