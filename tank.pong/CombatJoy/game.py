import pygame
from pygame.locals import *

import arena
import tank
import projectile
from config import *
from collision import collide_with_wall

pygame.init()
pygame.joystick.init()
Joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
print(Joysticks)

# font
font = pygame.font.Font('assets/PressStart2P.ttf', 45)

# hud
hud1_text = font.render("3", True, cian)
hud2_text = font.render("3", True, purple)
hud1_text_rect = hud1_text.get_rect()
hud2_text_rect = hud2_text.get_rect()
hud1_text_rect.center = (250, 50)
hud2_text_rect.center = (650, 50)
score1 = 3
score2 = 3

# victory text
font = pygame.font.Font('assets/PressStart2P.ttf', 45)
victory_text1 = font.render("Blue player win", True, cian, black)
victory_text2 = font.render("Purple player win", True, purple, black)
victory_text1_rect = victory_text1.get_rect()
victory_text2_rect = victory_text2.get_rect()
victory_text1_rect.center = (450, 275)
victory_text2_rect.center = (450, 275)

# sounds
shoot_sound = pygame.mixer.Sound("assets/tiger.wav")
shoot_sound.set_volume(0.5)
tank_explode = pygame.mixer.Sound("assets/tank_explode.wav")
bounce_ball = pygame.mixer.Sound("assets/bounce_ball.wav")
tank_walk = pygame.mixer.Sound("assets/tank_walk.wav")
tank_walk.set_volume(0.5)
time_sound = tank_walk.get_length()
time_stop = 0

# screen
size = (900, 650)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("combat tank")

# controller

tank1 = tank.tank_player(pygame.image.load("assets/tank1.png"), 1, spawn_x_tank_1, spawn_y_tank_1)
tank2 = tank.tank_player(pygame.image.load("assets/tank2.png"), 2, spawn_x_tank_2, spawn_y_tank_2)
players = [tank1, tank2]

clock = pygame.time.Clock()

loop = True
recharge = False
no_animation = True
stop = False
victory1 = False
victory2 = False
respawn = False
time = 0
current_x = 0
current_y = 0
collide_time = 0
angle = 0

if stage_select == 0:

    background = pygame.image.load("assets/city_map.png")
    background.get_rect().center = (0, 0)
    screen.blit(background, background.get_rect())

else:

    background = pygame.image.load("assets/vegetation_map.png")
    background.get_rect().center = (0, 0)
    screen.blit(background, background.get_rect())

obstacles = arena.arena()
obstacles.make_arena(screen, orange, stage_select)

while loop:
    time = pygame.time.get_ticks()
    screen.blit(background, background.get_rect())

    for event in pygame.event.get():
        if event.type == JOYBUTTONDOWN:
            if event.button == pygame.joystick.Joystick(0).get_button(1) and (not tank2.get_reloading()):
                tank2.set_fire(True)
                tank2.set_reloading(True)
                tank2.set_reload_time(pygame.time.get_ticks())

            if event.button == pygame.joystick.Joystick(1).get_button(1) and (not tank1.get_reloading()):
                tank1.set_fire(True)
                tank1.set_reloading(True)
                tank1.set_reload_time(pygame.time.get_ticks())

        if event.type == JOYHATMOTION:
            if pygame.joystick.Joystick(0).get_hat(0) == (0, 1):
                tank2.set_forward(True)
            if pygame.joystick.Joystick(0).get_hat(0) == (1, 0):
                tank2.set_turn_right(True)
            if pygame.joystick.Joystick(0).get_hat(0) == (-1, 0):
                tank2.set_turn_left(True)
            if pygame.joystick.Joystick(0).get_hat(0) == (0, 0):
                tank2.set_forward(False)
                tank2.set_turn_right(False)
                tank2.set_turn_left(False)

            if pygame.joystick.Joystick(1).get_hat(0) == (0, 1):
                tank1.set_forward(True)
            if pygame.joystick.Joystick(1).get_hat(0) == (1, 0):
                tank1.set_turn_right(True)
            if pygame.joystick.Joystick(1).get_hat(0) == (-1, 0):
                tank1.set_turn_left(True)
            if pygame.joystick.Joystick(1).get_hat(0) == (0, 0):
                tank1.set_forward(False)
                tank1.set_turn_right(False)
                tank1.set_turn_left(False)

        if event.type == pygame.QUIT:
            loop = False

        # configuring game keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                tank2.set_forward(True)
            if event.key == pygame.K_RIGHT:
                tank2.set_turn_right(True)
            if event.key == pygame.K_LEFT:
                tank2.set_turn_left(True)
            if event.key == pygame.K_l and (not tank2.get_reloading()):
                tank2.set_fire(True)
                tank2.set_reloading(True)
                tank2.set_reload_time(pygame.time.get_ticks())

            if event.key == pygame.K_w:
                tank1.set_forward(True)
            if event.key == pygame.K_d:
                tank1.set_turn_right(True)
            if event.key == pygame.K_a:
                tank1.set_turn_left(True)
            if event.key == pygame.K_t and (not tank1.get_reloading()):
                tank1.set_fire(True)
                tank1.set_reloading(True)
                tank1.set_reload_time(pygame.time.get_ticks())

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                tank2.set_forward(False)
            if event.key == pygame.K_RIGHT:
                tank2.set_turn_right(False)
            if event.key == pygame.K_LEFT:
                tank2.set_turn_left(False)

            if event.key == pygame.K_w:
                tank1.set_forward(False)
            if event.key == pygame.K_d:
                tank1.set_turn_right(False)
            if event.key == pygame.K_a:
                tank1.set_turn_left(False)

    if no_animation and not victory1 and not victory2:
        for tank in players:
            if tank.get_player_id() == 1:
                tank_enemy = players[1]
            else:
                tank_enemy = players[0]

            # reloading
            if time - tank.get_reload_time() > time_limit:
                tank.set_reloading(False)

            # player movement
            tank.move()
            if tank.get_forward() or tank.get_turn_right() or tank.get_turn_left():
                if time - time_stop > time_sound * 1000:
                    tank_walk.play()
                    time_stop = pygame.time.get_ticks()

            tank.set_rect(tank.get_surface().get_rect())
            tank.set_rect_center(tank.get_current_x(), tank.get_current_y())
            screen.blit(tank.get_surface(), tank.get_rect())

            if time - tank.get_reload_time() > time_limit:
                tank.set_reloading(False)

            # Shot a projectile
            if tank.get_fire():
                tank.set_fire(False)
                shoot_sound.play()
                tank.add_projectile(projectile.projectile(pygame.image.load("assets/bala.png"), tank.get_speed(),
                                                          tank.get_current_x(), tank.get_current_y(), screen))
            # projectile movement
            for shot in tank.get_projectiles():
                shot.move()

            if respawn:
                players[0].clear_projectiles()
                players[0].set_current_x(players[0].get_spawn_x())
                players[0].set_current_y(players[0].get_spawn_y())

                players[1].clear_projectiles()
                players[1].set_current_x(players[1].get_spawn_x())
                players[1].set_current_y(players[1].get_spawn_y())

                respawn = False

            # drawing arena and checking collision of the blocks with tanks
            for element in obstacles.get_obstacles():
                screen.blit(element.get_asset(), element.get_rect())

                if tank.get_rect().colliderect(element.get_rect()):
                    pos = element.get_position()
                    size = element.get_size()
                    pos_speed = collide_with_wall(tank, pos[0], pos[1], size[0], size[1], 0)

                    if tank.get_current_x() != pos_speed[0][0]:
                        tank.set_current_x(pos_speed[0][0])

                    if tank.get_current_y() != pos_speed[0][1]:
                        tank.set_current_y(pos_speed[0][1])

                for bullet in tank_enemy.get_projectiles():
                    screen.blit(bullet.get_asset(), bullet.get_rect())
                    if bullet.get_rect().colliderect(element.get_rect()):
                        pos = element.get_position()
                        size = element.get_size()
                        bullet.set_lives(bullet.get_lives()-1)
                        bounce_ball.play()
                        pos_speed = collide_with_wall(bullet, pos[0], pos[1], size[0], size[1], 1)
                        bullet.set_x_pos(pos_speed[0][0])
                        bullet.set_y_pos(pos_speed[0][1])
                        bullet.set_speed_x(pos_speed[1][0])
                        bullet.set_speed_y(pos_speed[1][1])

                    if bullet.get_lives() <= 0:
                        tank_enemy.get_projectiles().remove(bullet)

                    if bullet.get_rect().colliderect(tank.get_rect()):
                        tank.set_got_shot(1)
                        bullet.set_lives(0)
                        current_x = tank.get_current_x()
                        current_y = tank.get_current_y()
                        respawn = True
                        no_animation = False
                        stop = True
                        tank_explode.play()
                        collide_time = pygame.time.get_ticks()

    if not no_animation and not victory1 and not victory2:
        if time - collide_time >= 2000:
            no_animation = True
            if players[0].get_got_shot() == 1:
                players[0].live_lost()
                players[0].set_got_shot(0)
            elif players[1].get_got_shot() == 1:
                players[1].live_lost()
                players[1].set_got_shot(0)
        for element in obstacles.get_obstacles():
            screen.blit(element.get_asset(), element.get_rect())

        if players[0].get_got_shot() == 1:
            angle += 18
            tank_p = pygame.transform.rotate(players[0].get_asset(), angle)
            tank_animation_rect = players[0].get_asset().get_rect()
            tank_animation_rect.center = (current_x, current_y)
            screen.blit(tank_p, tank_animation_rect)
            screen.blit(players[1].get_surface(), players[1].get_rect())

        elif players[1].get_got_shot() == 1:
            angle += 18
            tank_p = pygame.transform.rotate(players[1].get_asset(), angle)
            tank_animation_rect = players[1].get_asset().get_rect()
            tank_animation_rect.center = (current_x, current_y)
            screen.blit(tank_p, tank_animation_rect)
            screen.blit(players[0].get_surface(), players[0].get_rect())

    if players[1].get_lives() <= 0:
        victory1 = True
    if players[0].get_lives() <= 0:
        victory2 = True

    # draw hud
    hud1_text = font.render(str(players[0].get_lives()), True, cian)
    hud2_text = font.render(str(players[1].get_lives()), True, purple)
    screen.blit(hud1_text, hud1_text_rect)
    screen.blit(hud2_text, hud2_text_rect)

    if victory1:
        screen.fill(black)
        screen.blit(victory_text1, victory_text1_rect)
    if victory2:
        screen.fill(black)
        screen.blit(victory_text2, victory_text2_rect)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
