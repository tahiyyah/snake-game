import pygame
from pygame import *
import random

pygame.init()

screen_width, screen_height = 600, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("snake")
clock = pygame.time.Clock()

block = 20

class Snake():
    def __init__(self):
        self.x, self.y = 300, 300 #starting coordinates
        self.direction_x = 1 #1 for right, -1 for left
        self.direction_y = 0 #1 for down, -1 for up
        self.head = pygame.Rect(self.x, self.y, block, block)
        self.body = [pygame.Rect(self.x - block, self.y, block, block)]
        self.dead = False
        self.score = 0

    def update(self):
        self.body.append(self.head)
        for i in range(len(self.body)-1):
            self.body[i].x = self.body[i+1].x #so body follows head
            self.body[i].y = self.body[i+1].y
        self.head.x += self.direction_x * block
        self.head.y += self.direction_y * block
        self.body.remove(self.head)

        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y: #if collides with block in body
                self.dead = True
            if self.head.x not in range(0, screen_width) or self.head.y not in range(0, screen_height): #if outside screen
                self.dead = True

        if self.dead: #resets all attributes
            self.x, self.y = block, block
            self.head = pygame.Rect(self.x, self.y, block, block)
            self.body = [pygame.Rect(self.x - block, self.y, block, block)]
            self.direction_x = 1
            self.direction_y = 0
            self.dead = False
            self.score = 0

class Apple():
    def __init__(self):
        self.x = int(random.randint(0, screen_width/block)) * block #so blocks generate in line with the head
        self.y = int(random.randint(0, screen_height/block)) * block
        self.rect = pygame.Rect(self.x, self.y, block, block)

    def update(self):
        pygame.draw.rect(screen, 'red', self.rect)

snake = Snake() #instantiating objects
apple = Apple()

while True:
    #draw to screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    keys = pygame.key.get_pressed() #movement
    if keys[pygame.K_RIGHT] and snake.direction_x != -1:
        snake.direction_x = 1
        snake.direction_y = 0
    if keys[pygame.K_LEFT] and snake.direction_x != 1:
        snake.direction_x = -1
        snake.direction_y = 0
    if keys[pygame.K_DOWN] and snake.direction_y != -1:
        snake.direction_x = 0
        snake.direction_y = 1
    if keys[pygame.K_UP] and snake.direction_y != 1:
        snake.direction_x = 0
        snake.direction_y = -1

    snake.update()
    screen.fill('black')
    apple.update()
    
    font = pygame.font.SysFont('Arial', 20) #blits score to screen
    text = font.render('score: '+str(snake.score), True, 'white')
    screen.blit(text, (20, 20))

    pygame.draw.rect(screen, 'green', snake.head) #drawing snake to screen
    pygame.draw.ellipse(screen, 'blue', snake.head)
    for square in snake.body:
        pygame.draw.rect(screen, 'green', square)

    if snake.head.x == apple.rect.x and snake.head.y == apple.rect.y: #if head collides with apple
        snake.score += 1
        snake.body.append(pygame.Rect(square.x, square.y, block, block)) #adds a block to body
        apple = Apple() #generates new apple
        apple.update()

    pygame.display.update()
    clock.tick(10)
