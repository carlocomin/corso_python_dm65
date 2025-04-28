import pygame, sys, time

LARGHEZZA, ALTEZZA = 800, 600
BIANCO = (255, 255, 255)
NERO = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Pong Velocità Dinamica")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

# Paddle
paddle = pygame.Rect(30, ALTEZZA//2 - 60, 10, 120)
cpu = pygame.Rect(LARGHEZZA - 40, ALTEZZA//2 - 60, 10, 120)
vel_paddle, vel_cpu = 7, 7

# Palla
ball = pygame.Rect(LARGHEZZA//2, ALTEZZA//2, 15, 15)
vel_x, vel_y = 7, 7
velocita_palla = 7

# Punteggio
punti_giocatore, punti_cpu = 0, 0

# Timer per velocità
tempo_inizio = pygame.time.get_ticks()
countdown = 10

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimento paddle giocatore
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and paddle.top > 0:
        paddle.y -= vel_paddle
    if keys[pygame.K_DOWN] and paddle.bottom < ALTEZZA:
        paddle.y += vel_paddle

    # Movimento CPU
    if cpu.centery < ball.centery and cpu.bottom < ALTEZZA:
        cpu.y += vel_cpu
    if cpu.centery > ball.centery and cpu.top > 0:
        cpu.y -= vel_cpu

    # Movimento palla
    ball.x += vel_x
    ball.y += vel_y

    # Collisioni bordi
    if ball.top <= 0 or ball.bottom >= ALTEZZA:
        vel_y *= -1

    # Collisioni paddle
    if ball.colliderect(paddle) or ball.colliderect(cpu):
        vel_x *= -1

    # Punto segnato
    if ball.left <= 0:
        punti_cpu += 1
        ball.center = (LARGHEZZA//2, ALTEZZA//2)
        vel_x = -velocita_palla
        vel_y = velocita_palla
        tempo_inizio = pygame.time.get_ticks()
        countdown = 10
    if ball.right >= LARGHEZZA:
        punti_giocatore += 1
        ball.center = (LARGHEZZA//2, ALTEZZA//2)
        vel_x = velocita_palla
        vel_y = -velocita_palla
        tempo_inizio = pygame.time.get_ticks()
        countdown = 10

    # Timer velocità
    tempo_ora = pygame.time.get_ticks()
    elapsed_sec = (tempo_ora - tempo_inizio) // 1000
    if elapsed_sec >= 10:
        velocita_palla += 1
        vel_x = velocita_palla if vel_x > 0 else -velocita_palla
        vel_y = velocita_palla if vel_y > 0 else -velocita_palla
        tempo_inizio = pygame.time.get_ticks()
        countdown = 10
    else:
        countdown = 10 - elapsed_sec

    # Disegna tutto
    screen.fill(NERO)
    pygame.draw.rect(screen, BIANCO, paddle)
    pygame.draw.rect(screen, BIANCO, cpu)
    pygame.draw.ellipse(screen, BIANCO, ball)
    pygame.draw.aaline(screen, BIANCO, (LARGHEZZA//2, 0), (LARGHEZZA//2, ALTEZZA))

    testo = font.render(f"{punti_giocatore} - {punti_cpu}", True, BIANCO)
    screen.blit(testo, (LARGHEZZA//2 - 60, 20))

    vel_text = font.render(f"Vel: {velocita_palla}", True, BIANCO)
    screen.blit(vel_text, (LARGHEZZA//2 + 60, 20))

    cd_text = font.render(f"⏱ {countdown}", True, BIANCO)
    screen.blit(cd_text, (LARGHEZZA//2 - 30, 60))

    pygame.display.update()
    clock.tick(60)
