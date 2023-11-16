import pygame
from config import UNIT_SIZE, SPEED

class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, image: pygame.Surface, screen: pygame.Surface):
        self.x = x
        self.y = y
        self.image = image
        self.area = pygame.Rect(self.x, self.y, UNIT_SIZE, UNIT_SIZE)
        self.screen = screen

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

    def move(self, x, y):
        self.x += x
        self.y += y
        self.area = pygame.Rect(self.x, self.y, UNIT_SIZE, UNIT_SIZE)
        
    def makeMove(self, dir):
        if dir == 'left':
            self.move(-SPEED, 0)
        if dir == 'right':
            self.move(SPEED, 0)
        if dir == 'up':
            self.move(0, -SPEED)
        if dir == 'down':
            self.move(0, SPEED)