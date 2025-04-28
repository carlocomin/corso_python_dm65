import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Sprite Demo")

sprite = pygame.image.load("robot_sprite.png")
sprite = pygame.transform.scale(sprite, (80, 80))
x, y = 200, 200
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((240, 248, 255))  # Colore sfondo
    screen.blit(sprite, (x, y))   # Disegna sprite
    pygame.display.update()
    clock.tick(60)

pygame.quit()