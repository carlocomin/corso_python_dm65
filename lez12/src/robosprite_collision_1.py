import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

robot = pygame.image.load("robot_sprite.png")
robot = pygame.transform.scale(robot, (80, 80))
robot_x, robot_y = 50, 50
vel = 5

ostacolo = pygame.Rect(300, 200, 100, 100)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    tasti = pygame.key.get_pressed()
    if tasti[pygame.K_RIGHT]: robot_x += vel
    if tasti[pygame.K_LEFT]:  robot_x -= vel
    if tasti[pygame.K_DOWN]:  robot_y += vel
    if tasti[pygame.K_UP]:    robot_y -= vel

    screen.fill((240, 248, 255))
    screen.blit(robot, (robot_x, robot_y))
    pygame.draw.rect(screen, (255, 100, 100), ostacolo)

    # Collisione
    robot_rect = pygame.Rect(robot_x, robot_y, 80, 80)
    if robot_rect.colliderect(ostacolo):
        print("Collisione!")

    pygame.display.update()
    clock.tick(60)

pygame.quit()