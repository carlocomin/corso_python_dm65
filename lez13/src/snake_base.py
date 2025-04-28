import pygame
import sys

# Configurazione griglia
LARGHEZZA, ALTEZZA = 600, 400
DIMENSIONE_BLOCCO = 20
FPS = 10

# Colori
VERDE = (0, 255, 0)
NERO = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

# Posizione iniziale della testa
x, y = LARGHEZZA // 2, ALTEZZA // 2
dx, dy = DIMENSIONE_BLOCCO, 0  # Direzione iniziale: destra

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                dx, dy = 0, -DIMENSIONE_BLOCCO
            elif event.key == pygame.K_DOWN:
                dx, dy = 0, DIMENSIONE_BLOCCO
            elif event.key == pygame.K_LEFT:
                dx, dy = -DIMENSIONE_BLOCCO, 0
            elif event.key == pygame.K_RIGHT:
                dx, dy = DIMENSIONE_BLOCCO, 0

    # Movimento
    x += dx
    y += dy

    screen.fill(NERO)
    pygame.draw.rect(screen, VERDE, (x, y, DIMENSIONE_BLOCCO, DIMENSIONE_BLOCCO))
    pygame.display.update()
    clock.tick(FPS)