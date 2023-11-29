import pygame
from config import *


class tank_player:
    def __init__(self, asset, player_number, spawn_x_pos, spawn_y_pos):
        self.asset = asset
        self.surface = pygame.Surface((self.asset.get_width(), self.asset.get_height()))
        self.surface.set_colorkey(orange)
        pygame.draw.rect(self.surface, orange, (0, 0, *self.asset.get_size()))
        self.surface.blit(self.asset, (0, 0))
        self.spawn_x = spawn_x_pos
        self.spawn_y = spawn_y_pos
        self.current_x = spawn_x_pos
        self.current_y = spawn_y_pos
        self.angle = 0
        self.forward = False
        self.turn_right = False
        self.turn_left = False
        self.fire = False
        self.reloading = False
        self.reload_time = 0
        self.speed = pygame.math.Vector2((speed_x_tanks, speed_y_tanks))
        self.projectiles = []
        self.lives = 3
        self.got_shot = 0
        self.player = player_number
        self.rect = self.asset.get_rect()
        self.rect.center = (self.current_x, self.current_y)

    def get_asset(self):
        return self.asset

    def get_surface(self):
        return self.surface

    def get_spawn_x(self):
        return self.spawn_x

    def get_spawn_y(self):
        return self.spawn_y

    def get_current_x(self):
        return self.current_x

    def get_current_y(self):
        return self.current_y

    def get_angle(self):
        return self.angle

    def get_forward(self):
        return self.forward

    def get_turn_right(self):
        return self.turn_right

    def get_turn_left(self):
        return self.turn_left

    def get_fire(self):
        return self.fire

    def get_reloading(self):
        return self.reloading

    def get_reload_time(self):
        return self.reload_time

    def get_speed(self):
        return self.speed

    def get_projectiles(self):
        return self.projectiles

    def get_lives(self):
        return self.lives

    def get_got_shot(self):
        return self.got_shot

    def get_player_id(self):
        return self.player

    def get_rect(self):
        return self.rect

    def set_asset(self, new_asset):
        self.asset = new_asset

    def set_surface(self, new_surface):
        self.surface = new_surface

    def set_spawn_x(self, new_spawn_x):
        self.spawn_x = new_spawn_x

    def set_spawn_y(self, new_spawn_y):
        self.spawn_y = new_spawn_y

    def set_current_x(self, new_x_pos):
        self.current_x = new_x_pos

    def set_current_y(self, new_y_pos):
        self.current_y = new_y_pos

    def set_angle(self, new_angle):
        self.angle = new_angle

    def set_forward(self, forward):
        self.forward = forward

    def set_turn_right(self, turn_right):
        self.turn_right = turn_right

    def set_turn_left(self, turn_left):
        self.turn_left = turn_left

    def set_fire(self, fire):
        self.fire = fire

    def set_reloading(self, reloading):
        self.reloading = reloading

    def set_reload_time(self, reload_time):
        self.reload_time = reload_time

    def set_speed(self, speed):
        self.speed = speed

    def reset_speed(self):
        self.speed = pygame.math.Vector2((speed_x_tanks, speed_y_tanks))

    def add_projectile(self, projectile):
        self.projectiles.append(projectile)

    def set_lives(self, lives):
        self.lives = lives

    def set_got_shot(self, shot):
        self.got_shot = shot

    def set_rect(self, rect):
        self.rect = rect

    def set_rect_center(self, x, y):
        self.rect.center = (x, y)

    def clear_projectiles(self):
        self.projectiles.clear()

    def live_lost(self):
        self.lives -= 1

    def move(self):
        if self.get_forward() and not self.get_turn_right() and not self.get_turn_left():
            self.set_current_x(self.get_current_x() + self.get_speed()[0])
            self.set_current_y(self.get_current_y() + self.get_speed()[1])

        if self.get_turn_right() and not self.get_turn_left():
            self.set_angle(self.get_angle() - 1)
            if self.get_angle() <= -360:
                self.set_angle(0)
            self.set_surface(pygame.transform.rotate(self.get_asset(), self.get_angle()))
            self.set_speed(self.get_speed().rotate(1))

        if self.get_turn_left() and not self.get_turn_right():
            self.set_angle(self.get_angle() + 1)
            if self.get_angle() >= 360:
                self.set_angle(0)
            self.set_surface(pygame.transform.rotate(self.get_asset(), self.get_angle()))
            self.set_speed(self.get_speed().rotate(-1))

        self.set_rect(self.get_surface().get_rect())
        self.set_rect_center(self.get_current_x(), self.get_current_y())

    def shoot(self, projectile):
        self.add_projectile(projectile)
