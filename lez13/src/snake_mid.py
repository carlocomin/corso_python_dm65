import pygame, sys, random

LARGHEZZA, ALTEZZA = 600, 400
DIMENSIONE_BLOCCO = 20
FPS = 10

VERDE = (0, 255, 0)
ROSSO = (255, 0, 0)
NERO = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

# Serpente iniziale
snake = [(LARGHEZZA//2, ALTEZZA//2)]
dx, dy = DIMENSIONE_BLOCCO, 0

# Cibo iniziale
cibo = (random.randrange(0, LARGHEZZA, DIMENSIONE_BLOCCO),
        random.randrange(0, ALTEZZA, DIMENSIONE_BLOCCO))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and dy == 0:
                dx, dy = 0, -DIMENSIONE_BLOCCO
            elif event.key == pygame.K_DOWN and dy == 0:
                dx, dy = 0, DIMENSIONE_BLOCCO
            elif event.key == pygame.K_LEFT and dx == 0:
                dx, dy = -DIMENSIONE_BLOCCO, 0
            elif event.key == pygame.K_RIGHT and dx == 0:
                dx, dy = DIMENSIONE_BLOCCO, 0

    # Nuova posizione testa
    x, y = snake[0]
    nuova_testa = (x + dx, y + dy)

    # Controllo collisioni
    if (nuova_testa in snake or
        nuova_testa[0] < 0 or nuova_testa[0] >= LARGHEZZA or
        nuova_testa[1] < 0 or nuova_testa[1] >= ALTEZZA):
        pygame.quit()
        sys.exit()

    snake.insert(0, nuova_testa)

    # Mangia cibo?
    if nuova_testa == cibo:
        cibo = (random.randrange(0, LARGHEZZA, DIMENSIONE_BLOCCO),
                random.randrange(0, ALTEZZA, DIMENSIONE_BLOCCO))
    else:
        snake.pop()

    # Disegno
    screen.fill(NERO)
    for blocco in snake:
        pygame.draw.rect(screen, VERDE, (*blocco, DIMENSIONE_BLOCCO, DIMENSIONE_BLOCCO))
    pygame.draw.rect(screen, ROSSO, (*cibo, DIMENSIONE_BLOCCO, DIMENSIONE_BLOCCO))
    pygame.display.update()
    clock.tick(FPS)