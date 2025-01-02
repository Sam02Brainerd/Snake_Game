import sys
import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 450
UI_HEIGHT = 50
PLAY_AREA_HEIGHT = HEIGHT - UI_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GRAY = (169, 169, 169)
GREEN = (0, 255, 0)

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Font for displaying text
font = pygame.font.SysFont("bahnschrift", 25)

# Snake speed (default speed)
snake_speed = 5

def draw_button(text, x, y, width, height, color, text_color):
    """Draws a button with text."""
    pygame.draw.rect(screen, color, (x, y, width, height))
    label = font.render(text, True, text_color)
    label_rect = label.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(label, label_rect)

def show_dialog_box(message, score, button1_text, button2_text, button1_action, button2_action):
    """Displays a dialog box with two buttons."""
    dialog_width, dialog_height = 300, 200
    dialog_x, dialog_y = (WIDTH - dialog_width) // 2, (HEIGHT - dialog_height) // 2

    pygame.draw.rect(screen, GRAY, (dialog_x, dialog_y, dialog_width, dialog_height))
    pygame.draw.rect(screen, WHITE, (dialog_x + 10, dialog_y + 10, dialog_width - 20, dialog_height - 20))

    # Display message and score
    message_text = font.render(message, True, BLACK)
    score_text = font.render(f"Your Score: {score}", True, BLACK)
    message_rect = message_text.get_rect(center=(WIDTH // 2, dialog_y + 40))
    score_rect = score_text.get_rect(center=(WIDTH // 2, dialog_y + 80))
    screen.blit(message_text, message_rect)
    screen.blit(score_text, score_rect)

    # Draw buttons
    button1_x, button1_y = dialog_x + 30, dialog_y + 140
    button2_x, button2_y = dialog_x + dialog_width - 130, dialog_y + 140

    draw_button(button1_text, button1_x, button1_y, 100, 40, GREEN, BLACK)
    draw_button(button2_text, button2_x, button2_y, 100, 40, RED, BLACK)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if button1_x < mouse_pos[0] < button1_x + 100 and button1_y < mouse_pos[1] < button1_y + 40:
                    button1_action()
                    return
                if button2_x < mouse_pos[0] < button2_x + 100 and button2_y < mouse_pos[1] < button2_y + 40:
                    button2_action()
                    return

        pygame.display.update()

def start_screen():
    """Displays the main menu with a 'Start Game' button."""
    screen.fill(BLACK)
    title_text = font.render("Welcome to Snake Game", True, ORANGE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(title_text, title_rect)

    draw_button("Start Game", WIDTH // 2 - 75, HEIGHT // 2, 150, 50, GREEN, BLACK)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH // 2 - 75 < mouse_pos[0] < WIDTH // 2 + 75 and HEIGHT // 2 < mouse_pos[1] < HEIGHT // 2 + 50:
                    return

def game_loop():
    global snake_speed

    def restart_game():
        global snake_speed
        snake_speed = 5  # Reset snake speed to the default value
        game_loop()  # Restart the game loop

    def quit_game():
        pygame.quit()
        sys.exit()

    x1, y1 = WIDTH // 2, PLAY_AREA_HEIGHT // 2
    x1_change, y1_change = 0, 0
    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, WIDTH - 10) / 10.0) * 10.0
    foody = round(random.randrange(UI_HEIGHT, HEIGHT - 10) / 10.0) * 10.0

    score = 0
    direction = None
    is_paused = False

    def display_ui(score):
        pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, UI_HEIGHT))
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        draw_button("Pause", WIDTH - 110, 10, 100, 30, BLACK, WHITE)

    def draw_snake(snake_list):
        head = snake_list[-1]
        pygame.draw.ellipse(screen, ORANGE, [head[0] - 5, head[1] - 10, 20, 20])
        for segment in snake_list[:-1]:
            pygame.draw.circle(screen, ORANGE, (segment[0] + 5, segment[1] + 5), 7)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and not is_paused:
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    x1_change, y1_change = -10, 0
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    x1_change, y1_change = 10, 0
                    direction = "RIGHT"
                elif event.key == pygame.K_UP and direction != "DOWN":
                    x1_change, y1_change = 0, -10
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    x1_change, y1_change = 0, 10
                    direction = "DOWN"

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH - 110 < mouse_pos[0] < WIDTH - 10 and 10 < mouse_pos[1] < 40:
                    show_dialog_box("Game Paused", score, "Resume", "Quit", lambda: None, quit_game)

        if not is_paused:
            x1 += x1_change
            y1 += y1_change

            if x1 >= WIDTH:
                x1 = 0
            elif x1 < 0:
                x1 = WIDTH - 10
            if y1 >= HEIGHT:
                y1 = UI_HEIGHT
            elif y1 < UI_HEIGHT:
                y1 = HEIGHT - 10

            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, WIDTH - 10) / 10.0) * 10.0
                foody = round(random.randrange(UI_HEIGHT, HEIGHT - 10) / 10.0) * 10.0
                length_of_snake += 1
                score += 10
                
                # Increase the snake speed after eating food (but limit the speed)
                if snake_speed < 30:  # Prevent the speed from getting too high
                    snake_speed += 1

            snake_head = [x1, y1]
            snake_list.append(snake_head)
            if len(snake_list) > length_of_snake:
                del snake_list[0]

            if snake_head in snake_list[:-1]:
                show_dialog_box("Game Over", score, "Restart", "Quit", restart_game, quit_game)

        screen.fill(BLACK)
        pygame.draw.circle(screen, RED, (int(foodx) + 5, int(foody) + 5), 7)
        draw_snake(snake_list)
        display_ui(score)
        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    sys.exit()


# Start the game
start_screen()
game_loop()
