import pygame
from arena import draw_arena
from collision import collision_tank_or_ball, collision_tank_bullet
from config import *

pygame.init()


# screen
size = (900, 650)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("combat tank")

list_two_tank = [tank1, tank2]
angle_tank = 0
image = 0
tank_animation_rect = 0
tank_animation_x, tank_animation_y, tank_enemy_photo, tank_enemy_rect = 0, 0, 0, 0

# objects

clock = pygame.time.Clock()

loop = True
recharge = False
no_animation = True
stop = False
victory1 = False
victory2 = False
time = 0

if stage_select == 0:

    background = pygame.image.load("assets/city_map.png")
    background.get_rect().center = (0, 0)
    screen.blit(background, background.get_rect())

else:

    background = pygame.image.load("assets/vegetation_map.png")
    background.get_rect().center = (0, 0)
    screen.blit(background, background.get_rect())

list_of_obstacles = draw_arena(screen, white, stage_select)

# game loop
while loop:
    respawn = False

    counter = pygame.time.get_ticks()
    screen.blit(background, background.get_rect())

    if no_animation and not victory1 and not victory2:
        for tank in list_two_tank:
            if stop:
                stop = False
                break
            tank_foto = tank[0]
            image = tank[1]
            origin_x = tank[2]
            origin_y = tank[3]
            tank_x = tank[4]
            tank_y = tank[5]
            angle_tank = tank[6]
            move = tank[7][0]
            giro_right = tank[7][1]
            giro_left = tank[7][2]
            tiro = tank[7][3]
            recharge = tank[7][4]
            recharge_time = tank[8]
            speed = tank[9]
            lista_de_bolas = tank[10]
            tank_life = tank[11]
            score = tank[12]
            if tank[12] == 1:
                tank_enemy_photo = list_two_tank[1][0]
                tank_enemy_rect = tank_enemy_photo.get_rect()
                tank_enemy_angle = list_two_tank[1][6]
                tank_enemy_surface = list_two_tank[1][1]
                tank_enemy_x = list_two_tank[1][4]
                tank_enemy_y = list_two_tank[1][5]
                tank_enemy_balls = list_two_tank[1][10]
                tank_enemy_rect.center = (tank_enemy_x, tank_enemy_y)
                tank_enemy_score = list_two_tank[1][12]
            else:
                tank_enemy_photo = list_two_tank[0][0]
                tank_enemy_rect = tank_enemy_photo.get_rect()
                tank_enemy_angle = list_two_tank[0][6]
                tank_enemy_surface = list_two_tank[0][1]
                tank_enemy_x = list_two_tank[0][4]
                tank_enemy_y = list_two_tank[0][5]
                tank_enemy_balls = list_two_tank[0][10]
                tank_enemy_rect.center = (tank_enemy_x, tank_enemy_y)
                tank_enemy_score = list_two_tank[0][12]

            if counter - recharge_time > time_limit:
                tank[7][4] = False

            speed = tank[9]

            # taking tank1's location
            tank_rect = tank_foto.get_rect()
            tank_rect.center = (tank[4], tank[5])

            # tank collision and draw obstacle
            tank_x = tank[4]
            tank_y = tank[5]
            comparison_x = tank[4]
            comparison_y = tank[5]
            for element in list_of_obstacles:
                obstacle_bit = element[0]
                obstacle_rect_idx = element[1]
                pos = element[2]
                screen.blit(obstacle_bit, obstacle_rect_idx)
                size = obstacle_bit.get_size()
                if tank_rect.colliderect(obstacle_rect_idx):
                    tup = collision_tank_or_ball(
                        tank_x, tank_y, speed[0], speed[1], pos[0], pos[1], size[0], size[1], 0
                    )
                    if comparison_x != tup[0][0]:
                        tank[4] = tup[0][0]
                    if comparison_y != tup[0][1]:
                        tank[5] = tup[0][1]

            # ball collision with objects and wall
            lista_de_bolas = tank[10]
            for ball in tank_enemy_balls:
                ball_image = ball[0]
                ball_rect = ball[1]
                ball_x = ball[2]
                ball_y = ball[3]
                speed_ball_x = ball[4]
                speed_ball_y = ball[5]
                ball_life = ball[6]
                screen.blit(ball_image, ball_rect)
                for element in list_of_obstacles:
                    obstacle_bit = element[0]
                    obstacle_rect_idx = element[1]
                    pos = element[2]
                    size = obstacle_bit.get_size()
                    if ball_rect.colliderect(obstacle_rect_idx):
                        ball[6] -= 1
                        var = collision_tank_or_ball(
                            ball_x, ball_y, speed_ball_x, speed_ball_y, pos[0], pos[1], size[0], size[1], 1
                        )
                        bounce_ball.play()
                        ball[2] = var[0][0]
                        ball[3] = var[0][1]
                        ball[4] = var[1][0]
                        ball[5] = var[1][1]

                # turn animation True
                if ball_rect.colliderect(tank_rect):
                    respawn = collision_tank_bullet(ball[4], ball[5], tank[4], tank[5], tank[11])
                    ball[6] = 0
                    no_animation = False
                    stop = True
                    tank_explode.play()
                    angle_tank = tank[6]
                    image = tank[1]
                    tank_animation_rect = tank[0].get_rect()
                    tank_animation_x = tank[4]
                    tank_animation_y = tank[5]
                    tank_p = tank[0]
                    tank[11] -= 1
                    time = pygame.time.get_ticks()

                if ball[6] <= 0:
                    tank_enemy_balls.remove(ball)

            if respawn:
                list_two_tank[0][10].clear()
                list_two_tank[0][4] = list_two_tank[0][2]
                list_two_tank[0][5] = list_two_tank[0][3]

                list_two_tank[1][10].clear()
                list_two_tank[1][4] = list_two_tank[1][2]
                list_two_tank[1][5] = list_two_tank[1][3]
                respawn = False

            screen.blit(tank_foto, tank_rect)
    if not no_animation and not victory1 and not victory2:
        if counter - time >= 2000:
            no_animation = True
        for obstacle in list_of_obstacles:
            obstacle_archive = obstacle[0]
            obstacle_rect = obstacle[1]
            screen.blit(obstacle_archive, obstacle_rect)
        angle_tank += 18
        tank_p = pygame.transform.rotate(image, angle_tank)
        tank_animation_rect.center = (tank_animation_x, tank_animation_y)
        screen.blit(tank_p, tank_animation_rect)
        screen.blit(tank_enemy_photo, tank_enemy_rect)
    if list_two_tank[1][11] <= 0:
        victory1 = True
    if list_two_tank[0][11] <= 0:
        victory2 = True

    # draw hud
    hud1_text = font.render(str(list_two_tank[0][11]), True, green)
    hud2_text = font.render(str(list_two_tank[1][11]), True, red)
    screen.blit(hud1_text, hud1_text_rect)
    screen.blit(hud2_text, hud2_text_rect)

    if victory1:
        screen.fill(black)
        screen.blit(victory_text1, victory_text1_rect)
    if victory2:
        screen.fill(black)
        screen.blit(victory_text2, victory_text2_rect)

    # update screen
    pygame.display.update()
    clock.tick(60)

pygame.quit()
