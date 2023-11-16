import pygame
from config import UNIT_SIZE

class Gold(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, image: pygame.Surface, screen: pygame.Surface):
        self.x = x
        self.y = y
        self.image = image
        self.area = pygame.Rect(self.x, self.y, UNIT_SIZE, UNIT_SIZE)
        self.screen = screen

    def draw(self):
        self.screen.blit(self.image, self.area)