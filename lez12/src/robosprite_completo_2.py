import pygame
import math
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Robot vs Nemici Intelligenti")

# Robot sprite
robot = pygame.image.load("robot_sprite.png")
robot = pygame.transform.scale(robot, (60, 60))
robot_rect = robot.get_rect()
robot_rect.topleft = (50, 270)

# Palla nemico sprite
nemico_sprite = pygame.image.load("spiked_ball.png")
nemico_sprite = pygame.transform.scale(nemico_sprite, (50, 50))

# Crea 5 nemici con posizioni iniziali fisse
nemici = []
posizioni_iniziali = [(700, 100), (700, 500), (400, 50), (400, 500), (600, 300)]
for pos in posizioni_iniziali:
    rect = nemico_sprite.get_rect()
    rect.topleft = pos
    nemici.append(rect)

# Ostacolo e traguardo
ostacolo = pygame.Rect(400, 250, 50, 100)
traguardo = pygame.Rect(750, 0, 50, 600)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

running = True
vittoria = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimento robot
    tasti = pygame.key.get_pressed()
    if tasti[pygame.K_RIGHT]:
        robot_rect.x += 5
    if tasti[pygame.K_LEFT]:
        robot_rect.x -= 5
    if tasti[pygame.K_UP]:
        robot_rect.y -= 5
    if tasti[pygame.K_DOWN]:
        robot_rect.y += 5

    # Movimento nemici con strategie diverse
    for i, nemico_rect in enumerate(nemici):
        dx, dy = 0, 0
        if i == 0:
            # Nemico 1: segue il robot
            dx = robot_rect.x - nemico_rect.x
            dy = robot_rect.y - nemico_rect.y
        elif i == 1:
            # Nemico 2: anticipa la posizione (previsione futura)
            dx = (robot_rect.x + 50) - nemico_rect.x
            dy = (robot_rect.y + 50) - nemico_rect.y
        elif i == 2:
            # Nemico 3: muove lateralmente (blocca a lato)
            dx = robot_rect.x - nemico_rect.x
            dy = 0
        elif i == 3:
            # Nemico 4: copre la via alta
            dx = robot_rect.x - nemico_rect.x
            dy = (robot_rect.y - 100) - nemico_rect.y
        elif i == 4:
            # Nemico 5: copre la via bassa
            dx = robot_rect.x - nemico_rect.x
            dy = (robot_rect.y + 100) - nemico_rect.y

        distanza = math.hypot(dx, dy)
        if distanza != 0:
            nemico_rect.x += int(4 * dx / distanza)
            nemico_rect.y += int(4 * dy / distanza)

    # Collisioni
    if robot_rect.colliderect(ostacolo) or any(robot_rect.colliderect(n) for n in nemici):
        running = False  # Game Over

    if robot_rect.colliderect(traguardo):
        vittoria = True
        running = False

    # Disegna
    screen.fill((240, 240, 255))
    pygame.draw.rect(screen, (255, 0, 0), ostacolo)
    pygame.draw.rect(screen, (0, 255, 0), traguardo)
    screen.blit(robot, robot_rect)
    for nemico_rect in nemici:
        screen.blit(nemico_sprite, nemico_rect)
    pygame.display.update()
    clock.tick(60)

# Messaggio finale
screen.fill((255, 255, 255))
msg = "VITTORIA!" if vittoria else "SEI STATO CIRCONDATO!"
text = font.render(msg, True, (0, 0, 0))
screen.blit(text, (250, 250))
pygame.display.update()
pygame.time.wait(2500)

pygame.quit()
