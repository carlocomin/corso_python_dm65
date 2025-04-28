import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Gioco del Robot")

# Carica sprite
robot = pygame.image.load("robot_sprite.png")
robot = pygame.transform.scale(robot, (60, 60))
robot_rect = robot.get_rect()
robot_rect.topleft = (50, 270)

# Ostacolo
ostacolo = pygame.Rect(400, 250, 50, 100)

# Traguardo
traguardo = pygame.Rect(750, 0, 50, 600)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

running = True
vittoria = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimento
    tasti = pygame.key.get_pressed()
    if tasti[pygame.K_RIGHT]:
        robot_rect.x += 5
    if tasti[pygame.K_LEFT]:
        robot_rect.x -= 5
    if tasti[pygame.K_UP]:
        robot_rect.y -= 5
    if tasti[pygame.K_DOWN]:
        robot_rect.y += 5

    # Collisioni
    if robot_rect.colliderect(ostacolo):
        running = False  # Game Over

    if robot_rect.colliderect(traguardo):
        vittoria = True
        running = False

    # Disegna tutto
    screen.fill((220, 240, 255))
    pygame.draw.rect(screen, (255, 0, 0), ostacolo)
    pygame.draw.rect(screen, (0, 255, 0), traguardo)
    screen.blit(robot, robot_rect)
    pygame.display.update()
    clock.tick(60)

# Messaggio finale
screen.fill((255, 255, 255))
msg = "VITTORIA!" if vittoria else "GAME OVER"
text = font.render(msg, True, (0, 0, 0))
screen.blit(text, (300, 250))
pygame.display.update()
pygame.time.wait(2000)

pygame.quit()