import pygame


class block:
    def __init__(self, asset, x, y, screen, color):
        self.asset = asset
        self.position = (x, y)
        self.size = asset.get_size()
        self.rect = pygame.draw.rect(screen, color, (self.position[0], self.position[1], self.asset.get_width(),
                                                     self.asset.get_height()))

    def get_asset(self):
        return self.asset

    def get_position(self):
        return self.position

    def get_size(self):
        return self.size

    def get_rect(self):
        return self.rect

    def set_asset(self, asset):
        self.asset = asset

    def set_position(self, position):
        self.position = position

    def set_size(self, size):
        self.size = size

    def set_rect(self, rect):
        self.rect = rect
