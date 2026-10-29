import pygame
import math
import random

win_width = 400
win_height = 400
cell_size = 20
clock = pygame.time.Clock()
dt = 0
screen = pygame.display.set_mode((win_width, win_height))
run = True

class Cell:
    __slots__ = ("x", "y", "world_x", "world_y", "space")

    def __init__(self, x, y, world_x, world_y):
        self.x = x
        self.y = y
        self.world_x = world_x
        self.world_y = world_y
        self.space = ""

class Grid:
    __slots__ = ("size", "width", "height", "spaces")

    def __init__(self, size, width, height):
        self.size = size
        self.width = width
        self.height = height
        self.spaces = []
        grid_x_count = self.width / self.size
        grid_y_count = self.height /self.size

        def convertToWorld(coord):
            return coord * self.size
        
        for grid_y in range(math.floor(grid_y_count)):
            for grid_x in range(math.floor(grid_x_count)):
                self.spaces.append(Cell(grid_x, grid_y, convertToWorld(grid_x), convertToWorld(grid_y)))


    def draw(self):
        for space in self.spaces:
            cell = pygame.Rect(space.world_x, space.world_y, cell_size, cell_size)
            pygame.draw.rect(screen, "white", cell, width = 1)

grid = Grid(cell_size, win_width, win_height)

class Segment:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

class Player:
    def __init__(self):
        self.body = [Segment(1, 1, cell_size), Segment(2, 1, cell_size), Segment(3, 1, cell_size)]
        self.timer = 0
        self.speed = 0.13
        self.direction = [1, 0]
        self.direction_queue = [[1, 0]]

    def move(self):
        if len(self.direction_queue) > 0:
            self.direction = self.direction_queue.pop()
        self.body.append(Segment(self.body[-1].x + self.direction[0], self.body[-1].y + self.direction[1], cell_size))
        self.body.pop(0)

    def control(self, keys):
        if keys[pygame.K_DOWN] and self.direction != [0, -1]:
            snake.direction_queue.append([0, 1])
        elif keys[pygame.K_UP] and self.direction != [0, 1]:
            snake.direction_queue.append([0, -1])
        elif keys[pygame.K_LEFT] and self.direction != [1, 0]:
            snake.direction_queue.append([-1, 0])
        elif keys[pygame.K_RIGHT] and self.direction != [-1, 0]:
            snake.direction_queue.append([1, 0])

    def eat(self):
        self.body.append(Segment(self.body[-1].x + self.direction[0], self.body[-1].y + self.direction[1], cell_size))


    def update(self, dt):
        self.timer += dt
        if self.timer > self.speed:
            self.move()
            self.timer = 0



    def draw(self):
        for segment in self.body:
            cell = pygame.Rect(segment.x * cell_size, segment.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, "green", cell)

snake = Player()

class Apple:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    
    def draw(self):
        rect = pygame.Rect(self.x * cell_size, self.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, "red", rect)

apples = [Apple(10, 10)]

while run:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    run = False

    screen.fill("black")

    keys = pygame.key.get_just_pressed()
    snake.control(keys)


    snake.update(dt)
    # print(snake.timer)

    grid.draw()

    snake.draw()

    for apple in apples:
        apple.draw()
        if apple.x == snake.body[-1].x and apple.y == snake.body[-1].y:
            apples.remove(apple)
            snake.eat()

    if len(apples) == 0:
        apples.append(Apple(random.randrange(0, math.floor(grid.width / cell_size)), random.randrange(0, math.floor(grid.height / cell_size))))



    pygame.display.flip()
    
    dt = clock.tick(60) / 1000

pygame.quit()
        