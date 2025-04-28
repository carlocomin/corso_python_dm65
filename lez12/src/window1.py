import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("FPS Demo")
clock = pygame.time.Clock()
FPS = 60

running = True
while running:
    clock.tick(FPS)  # Limita a 60 frame per secondo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((180, 220, 250))  # Blu pastello chiaro
    pygame.display.update()

pygame.quit()