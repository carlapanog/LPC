import pygame
import random
from config import *


class star:
    def __init__(self, asset, obstacles):
        self.asset = asset
        self.surface = pygame.Surface((self.asset.get_width(), self.asset.get_height()))
        self.surface.set_colorkey(orange)
        pygame.draw.rect(self.surface, orange, (0, 0, *self.asset.get_size()))
        self.surface.blit(self.asset, (0, 0))
        self.rect = self.asset.get_rect()
        self.x = 0
        self.y = 0
        self.obstacles = obstacles
        self.random_position()

    def get_rect(self):
        return self.rect

    def get_asset(self):
        return self.asset

    def get_surface(self):
        return self.surface

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def random_position(self):
        flag = True
        while flag:
            flag = False
            self.x = random.random() * 900.00
            self.y = 100 + random.random() * 550.00
            self.rect.center = (int(self.x), int(self.y))
            for element in self.obstacles.get_obstacles():
                if self.get_rect().colliderect(element.get_rect()):
                    flag = True
