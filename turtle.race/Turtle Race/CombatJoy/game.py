import pygame
from pygame.locals import *

import arena
import tank
import star
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
hud2_text = font.render("3", True, green)
hud1_text_rect = hud1_text.get_rect()
hud2_text_rect = hud2_text.get_rect()
hud1_text_rect.center = (250, 50)
hud2_text_rect.center = (650, 50)

# victory text
font = pygame.font.Font('assets/PressStart2P.ttf', 45)
victory_text1 = font.render("Blue player wins", True, cian, black)
victory_text2 = font.render("Green player wins", True, green, black)
victory_text1_rect = victory_text1.get_rect()
victory_text2_rect = victory_text2.get_rect()
victory_text1_rect.center = (450, 275)
victory_text2_rect.center = (450, 275)

# sounds
bounce_ball = pygame.mixer.Sound("assets/bounce_ball.wav")
turtle_walk = pygame.mixer.Sound("assets/turtle_walk.wav")
star_catch = pygame.mixer.Sound("assets/point.wav")
turtle_walk.set_volume(0.5)
time_sound = turtle_walk.get_length()
time_stop = 0

# screen
size = (900, 650)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("turtle race")

# controller
turtle1 = tank.TurtlePlayer(pygame.image.load("assets/turtle1.png"), 1, spawn_x_turtle_1, spawn_y_turtle_1)
turtle2 = tank.TurtlePlayer(pygame.image.load("assets/turtle2.png"), 2, spawn_x_turtle_2, spawn_y_turtle_2)
players = [turtle1, turtle2]

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

star = star.star(pygame.image.load("assets/star.png"), obstacles)

while loop:
    time = pygame.time.get_ticks()
    screen.blit(background, background.get_rect())

    for event in pygame.event.get():
        if event.type == JOYBUTTONDOWN:
            if event.button == pygame.joystick.Joystick(0).get_button(1) and (not turtle2.get_reloading()):
                turtle2.set_fire(True)
                turtle2.set_reloading(True)
                turtle2.set_reload_time(pygame.time.get_ticks())

            if event.button == pygame.joystick.Joystick(1).get_button(1) and (not turtle1.get_reloading()):
                turtle1.set_fire(True)
                turtle1.set_reloading(True)
                turtle1.set_reload_time(pygame.time.get_ticks())

        if event.type == JOYHATMOTION:
            if pygame.joystick.Joystick(0).get_hat(0) == (0, 1):
                turtle2.set_forward(True)
            if pygame.joystick.Joystick(0).get_hat(0) == (1, 0):
                turtle2.set_turn_right(True)
            if pygame.joystick.Joystick(0).get_hat(0) == (-1, 0):
                turtle2.set_turn_left(True)
            if pygame.joystick.Joystick(0).get_hat(0) == (0, 0):
                turtle2.set_forward(False)
                turtle2.set_turn_right(False)
                turtle2.set_turn_left(False)

            if pygame.joystick.Joystick(1).get_hat(0) == (0, 1):
                turtle1.set_forward(True)
            if pygame.joystick.Joystick(1).get_hat(0) == (1, 0):
                turtle1.set_turn_right(True)
            if pygame.joystick.Joystick(1).get_hat(0) == (-1, 0):
                turtle1.set_turn_left(True)
            if pygame.joystick.Joystick(1).get_hat(0) == (0, 0):
                turtle1.set_forward(False)
                turtle1.set_turn_right(False)
                turtle1.set_turn_left(False)

        if event.type == pygame.QUIT:
            loop = False

        # configuring game keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                turtle2.set_forward(True)
            if event.key == pygame.K_RIGHT:
                turtle2.set_turn_right(True)
            if event.key == pygame.K_LEFT:
                turtle2.set_turn_left(True)

            if event.key == pygame.K_w:
                turtle1.set_forward(True)
            if event.key == pygame.K_d:
                turtle1.set_turn_right(True)
            if event.key == pygame.K_a:
                turtle1.set_turn_left(True)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                turtle2.set_forward(False)
            if event.key == pygame.K_RIGHT:
                turtle2.set_turn_right(False)
            if event.key == pygame.K_LEFT:
                turtle2.set_turn_left(False)

            if event.key == pygame.K_w:
                turtle1.set_forward(False)
            if event.key == pygame.K_d:
                turtle1.set_turn_right(False)
            if event.key == pygame.K_a:
                turtle1.set_turn_left(False)

    if no_animation and not victory1 and not victory2:
        for turtle in players:
            if turtle.get_player_id() == 1:
                tank_enemy = players[1]
            else:
                tank_enemy = players[0]

            # player movement
            turtle.move()
            if turtle.get_forward() or turtle.get_turn_right() or turtle.get_turn_left():
                if time - time_stop > time_sound * 1000:
                    turtle_walk.play()
                    time_stop = pygame.time.get_ticks()
            star_rect = star.get_rect()
            screen.blit(star.get_asset(), star_rect)
            turtle.set_rect(turtle.get_surface().get_rect())
            turtle.set_rect_center(turtle.get_current_x(), turtle.get_current_y())
            screen.blit(turtle.get_surface(), turtle.get_rect())

            # drawing arena and checking collision of the blocks with turtles
            for element in obstacles.get_obstacles():
                screen.blit(element.get_asset(), element.get_rect())
                if turtle.get_rect().colliderect(element.get_rect()):
                    pos = element.get_position()
                    size = element.get_size()
                    pos_speed = collide_with_wall(turtle, pos[0], pos[1], size[0], size[1], 0)

                    if turtle.get_current_x() != pos_speed[0][0]:
                        turtle.set_current_x(pos_speed[0][0])

                    if turtle.get_current_y() != pos_speed[0][1]:
                        turtle.set_current_y(pos_speed[0][1])

            # checking collision of the star and turtles
            if turtle.get_rect().colliderect(star_rect):
                star_catch.play()
                star.random_position()
                turtle.score += 1

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

    if turtle1.score >= 3:
        victory1 = True
    if turtle2.score >= 3:
        victory2 = True

    # draw hud
    hud1_text = font.render(str(players[0].score), True, cian)
    hud2_text = font.render(str(players[1].score), True, green)
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
