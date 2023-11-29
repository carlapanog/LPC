import pygame
from config import *


class projectile:
    def __init__(self, asset, tank_speed, tank_x, tank_y, screen):
        self.asset = asset
        self.speed_x = speed_x_balls * tank_speed[0]
        self.speed_y = speed_y_balls * tank_speed[1]
        self.x_pos = tank_x
        self.y_pos = tank_y
        self.lives = 6
        self.rect = pygame.draw.rect(screen, white, (0, 0, self.asset.get_width(), self.asset.get_height()))
        self.rect.center = (self.x_pos, self.y_pos)

    def get_asset(self):
        return self.asset

    def get_speed_x(self):
        return self.speed_x

    def get_speed_y(self):
        return self.speed_y

    def get_x_pos(self):
        return self.x_pos

    def get_y_pos(self):
        return self.y_pos

    def get_lives(self):
        return self.lives

    def get_rect(self):
        return self.rect

    def get_rect_center(self):
        return self.rect.center

    def set_asset(self, asset):
        self.asset = asset

    def set_speed_x(self, speed_x):
        self.speed_x = speed_x

    def set_speed_y(self, speed_y):
        self.speed_y = speed_y

    def set_x_pos(self, x):
        self.x_pos = x

    def set_y_pos(self, y):
        self.y_pos = y

    def set_lives(self, lives):
        self.lives = lives

    def set_rect(self, rect):
        self.rect = rect

    def set_rect_center(self, center):
        self.rect.center = center

    def move(self):
        self.x_pos += self.speed_x
        self.y_pos += self.speed_y
        self.set_rect_center((self.x_pos, self.y_pos))
