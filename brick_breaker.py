import pygame
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Fonts
font = pygame.font.SysFont(None, 50)
small_font = pygame.font.SysFont(None, 36)

# Game States
HOME = "home"
PLAYING = "playing"
GAME_OVER = "game_over"
state = HOME

# Score & High Score
score = 0
high_score = 0

# Load high score from file
def load_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except:
        return 0

# Save high score to file
def save_high_score(new_score):
    with open("highscore.txt", "w") as file:
        file.write(str(new_score))

# Game Reset Function
def reset_game():
    global rect_x, ball_x, ball_y, ball_speed_vx, ball_speed_vy, bricks, score
    rect_width = 100
    rect_height = 10
    rect_x = WIDTH // 2
    rect_y = HEIGHT - rect_height

    ball_radius = 15
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_speed_vx = 4
    ball_speed_vy = 4

    brick_rows = 5
    brick_cols = 8
    brick_width = WIDTH // brick_cols
    brick_height = 30

    bricks = []
    for row in range(brick_rows):
        for col in range(brick_cols):
            brick_rect = pygame.Rect(col * brick_width, row * brick_height, brick_width - 2, brick_height - 2)
            bricks.append(brick_rect)

    score = 0
    return rect_width, rect_height, rect_x, rect_y, ball_radius, brick_width, brick_height

# Initial Game Values
rect_width, rect_height, rect_x, rect_y, ball_radius, brick_width, brick_height = reset_game()
high_score = load_high_score()

# Draw button
def draw_button(text, x, y, width, height):
    pygame.draw.rect(screen, GREEN, (x, y, width, height))
    txt = font.render(text, True, BLACK)
    txt_rect = txt.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(txt, txt_rect)
    return pygame.Rect(x, y, width, height)

# Game loop
running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle button clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()

            if state == HOME:
                if draw_button("Start", 320, 250, 160, 60).collidepoint(mx, my):
                    state = PLAYING
                    rect_width, rect_height, rect_x, rect_y, ball_radius, brick_width, brick_height = reset_game()

            elif state == GAME_OVER:
                if draw_button("Restart", 300, 300, 180, 60).collidepoint(mx, my):
                    state = PLAYING
                    rect_width, rect_height, rect_x, rect_y, ball_radius, brick_width, brick_height = reset_game()

    # ---------- HOME SCREEN ----------
    if state == HOME:
        title = font.render("Brick Breaker", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))
        draw_button("Start", 320, 250, 160, 60)

    # ---------- GAME PLAY ----------
    elif state == PLAYING:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            rect_x -= 5
        if keys[pygame.K_RIGHT]:
            rect_x += 5

        # Paddle boundary
        if rect_x < 0:
            rect_x = 0
        if rect_x + rect_width > WIDTH:
            rect_x = WIDTH - rect_width

        # Move ball
        ball_x += ball_speed_vx
        ball_y += ball_speed_vy

        # Wall collision
        if ball_x - ball_radius <= 0 or ball_x + ball_radius >= WIDTH:
            ball_speed_vx *= -1
        if ball_y - ball_radius <= 0:
            ball_speed_vy *= -1

        # Paddle collision
        if rect_y <= ball_radius + ball_y <= rect_y + rect_height and rect_x <= ball_x <= rect_x + rect_width:
            ball_speed_vy *= -1

        # Brick collision
        for brick in bricks[:]:
            if brick.collidepoint(ball_x, ball_y):
                bricks.remove(brick)
                ball_speed_vy *= -1
                score += 10
                break

        # Game over
        if ball_y - ball_radius > HEIGHT:
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            state = GAME_OVER

        # Draw game objects
        pygame.draw.rect(screen, RED, (rect_x, rect_y, rect_width, rect_height))
        pygame.draw.circle(screen, BLUE, (ball_x, ball_y), ball_radius)

        for brick in bricks:
            pygame.draw.rect(screen, GREEN, brick)

        # Draw score
        score_txt = small_font.render(f"Score: {score}", True, BLACK)
        high_score_txt = small_font.render(f"High Score: {high_score}", True, BLACK)
        screen.blit(score_txt, (10, 10))
        screen.blit(high_score_txt, (WIDTH - high_score_txt.get_width() - 10, 10))

    # ---------- GAME OVER SCREEN ----------
    elif state == GAME_OVER:
        over_txt = font.render("Game Over", True, BLACK)
        score_txt = font.render(f"Score: {score}", True, BLACK)
        high_score_txt = font.render(f"High Score: {high_score}", True, BLACK)
        screen.blit(over_txt, (WIDTH // 2 - over_txt.get_width() // 2, 150))
        screen.blit(score_txt, (WIDTH // 2 - score_txt.get_width() // 2, 230))
        screen.blit(high_score_txt, (WIDTH // 2 - high_score_txt.get_width() // 2, 280))
        draw_button("Restart", 300, 300, 180, 60)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
