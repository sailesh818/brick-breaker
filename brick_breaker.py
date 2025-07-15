import pygame
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker Game")

rect_width = 100
rect_height = 10
rect_x = WIDTH//2
rect_y = HEIGHT -rect_height
rect_speed = 5

ball_radius = 15
ball_x = WIDTH //2
ball_y = HEIGHT //2
ball_speed_vx = 4
ball_speed_vy = 4

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)

brick_rows = 5
brick_cols = 8
brick_width = WIDTH // brick_cols
brick_height = 30

bricks = []
for row in range(brick_rows):
    for col in range(brick_cols):
        brick_rect = pygame.Rect(col * brick_width, row * brick_height, brick_width -2, brick_height -2)
        bricks.append(brick_rect)


clock = pygame.time.Clock()
FPS = 60

running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        rect_x -= rect_speed
    if keys[pygame.K_RIGHT]:
        rect_x += rect_speed
        
    # Boundary settings
    if rect_x < 0:
        rect_x = 0 
    if rect_x + rect_width > WIDTH:
        rect_x = WIDTH - rect_width
        
    ball_x += ball_speed_vx
    ball_y += ball_speed_vy
    
    if ball_x  + ball_radius <= 0 or ball_x + ball_radius >= WIDTH:
        ball_speed_vx *= -1
    if ball_y - ball_radius <= 0:
        ball_speed_vy *= -1
    if (rect_y <= ball_radius + ball_y) and (rect_x <= ball_x <= rect_x + rect_width):
        ball_speed_vy *= -1 
        
    for brick in bricks[:]:
        if brick.collidepoint(ball_x, ball_y):
            bricks.remove(brick)
            ball_speed_vy *= -1
            break
    if ball_y - ball_radius > HEIGHT:
        print("GAME OVER")
        running = False
         
    pygame.draw.rect(screen, RED, (rect_x, rect_y, rect_width, rect_height))
    pygame.draw.circle(screen, BLUE, (ball_x, ball_y), ball_radius)
    
    for brick in bricks:
        pygame.draw.rect(screen, GREEN, brick)
            
    pygame.display.flip()
    clock.tick(FPS)
    
pygame.quit()
sys.exit()