import pygame

win_width = 400
win_height = 400
screen = pygame.display.set_mode((win_width, win_height))
run = True

player = [1, 1]


while run:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    run = False

    screen.fill("black")

    pygame.display.flip()

pygame.quit()
        