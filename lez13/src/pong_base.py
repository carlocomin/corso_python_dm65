import pygame, sys

LARGHEZZA, ALTEZZA = 800, 600
BIANCO = (255, 255, 255)
NERO = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

# Paddle
paddle = pygame.Rect(30, ALTEZZA//2 - 60, 10, 120)
vel_paddle = 5

# Palla
ball = pygame.Rect(LARGHEZZA//2, ALTEZZA//2, 15, 15)
vel_x, vel_y = 5, 5

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimento paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and paddle.top > 0:
        paddle.y -= vel_paddle
    if keys[pygame.K_DOWN] and paddle.bottom < ALTEZZA:
        paddle.y += vel_paddle

    # Movimento palla
    ball.x += vel_x
    ball.y += vel_y

    if ball.top <= 0 or ball.bottom >= ALTEZZA:
        vel_y *= -1

    screen.fill(NERO)
    pygame.draw.rect(screen, BIANCO, paddle)
    pygame.draw.ellipse(screen, BIANCO, ball)
    pygame.display.update()
    clock.tick(60)