import pygame
from arena import draw_arena
from collision import collision_turtle_or_ball, collision_turtle_bullet
from config import *

pygame.init()


# screen
size = (900, 650)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("turtle race")

list_two_turtle = [turtle1, turtle2]
angle_turtle = 0
image = 0
turtle_animation_rect = 0
turtle_animation_x, turtle_animation_y, turtle_enemy_photo, turtle_enemy_rect = 0, 0, 0, 0

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
        for turtle in list_two_turtle:
            if stop:
                stop = False
                break
            turtle_foto = turtle[0]
            image = turtle[1]
            origin_x = turtle[2]
            origin_y = turtle[3]
            tank_x = turtle[4]
            tank_y = turtle[5]
            angle_tank = turtle[6]
            move = turtle[7][0]
            giro_right = turtle[7][1]
            giro_left = turtle[7][2]
            tiro = turtle[7][3]
            recharge = turtle[7][4]
            recharge_time = turtle[8]
            speed = turtle[9]
            lista_de_bolas = turtle[10]
            turtle_life = turtle[11]
            score = turtle[12]
            if turtle[12] == 1:
                turtle_enemy_photo = list_two_turtle[1][0]
                turtle_enemy_rect = turtle_enemy_photo.get_rect()
                turtle_enemy_angle = list_two_turtle[1][6]
                turtle_enemy_surface = list_two_turtle[1][1]
                turtle_enemy_x = list_two_turtle[1][4]
                turtle_enemy_y = list_two_turtle[1][5]
                turtle_enemy_balls = list_two_turtle[1][10]
                turtle_enemy_rect.center = (turtle_enemy_x, turtle_enemy_y)
                turtle_enemy_score = list_two_turtle[1][12]
            else:
                turtle_enemy_photo = list_two_turtle[0][0]
                turtle_enemy_rect = turtle_enemy_photo.get_rect()
                turtle_enemy_angle = list_two_turtle[0][6]
                turtle_enemy_surface = list_two_turtle[0][1]
                turtle_enemy_x = list_two_turtle[0][4]
                turtle_enemy_y = list_two_turtle[0][5]
                turtle_enemy_balls = list_two_turtle[0][10]
                turtle_enemy_rect.center = (turtle_enemy_x, turtle_enemy_y)
                turtle_enemy_score = list_two_turtle[0][12]

            if counter - recharge_time > time_limit:
                turtle[7][4] = False

            speed = turtle[9]

            # taking turtle1's location
            tank_rect = turtle_foto.get_rect()
            tank_rect.center = (turtle[4], turtle[5])

            # turtle collision and draw obstacle
            turtle_x = turtle[4]
            turtle_y = turtle[5]
            comparison_x = turtle[4]
            comparison_y = turtle[5]
            for element in list_of_obstacles:
                obstacle_bit = element[0]
                obstacle_rect_idx = element[1]
                pos = element[2]
                screen.blit(obstacle_bit, obstacle_rect_idx)
                size = obstacle_bit.get_size()
                if turtle_rect.colliderect(obstacle_rect_idx):
                    tup = collision_turtle_or_ball(
                        turtle_x, turtle_y, speed[0], speed[1], pos[0], pos[1], size[0], size[1], 0
                    )
                    if comparison_x != tup[0][0]:
                        turtle[4] = tup[0][0]
                    if comparison_y != tup[0][1]:
                        turtle[5] = tup[0][1]

            # ball collision with objects and wall
            lista_de_bolas = turtle[10]
            for ball in turtle_enemy_balls:
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
                        var = collision_turtle_or_ball(
                            ball_x, ball_y, speed_ball_x, speed_ball_y, pos[0], pos[1], size[0], size[1], 1
                        )
                        bounce_ball.play()
                        ball[2] = var[0][0]
                        ball[3] = var[0][1]
                        ball[4] = var[1][0]
                        ball[5] = var[1][1]

                # turn animation True
                if ball_rect.colliderect(tank_rect):
                    respawn = collision_turtle_bullet(ball[4], ball[5], turtle[4], turtle[5], turtle[11])
                    ball[6] = 0
                    no_animation = False
                    stop = True
                    turtle_explode.play()
                    angle_turtle = turtle[6]
                    image = turtle[1]
                    turtle_animation_rect = turtle[0].get_rect()
                    turtle_animation_x = turtle[4]
                    turtle_animation_y = turtle[5]
                    turtle_p = turtle[0]
                    turtle[11] -= 1
                    time = pygame.time.get_ticks()

                if ball[6] <= 0:
                    turtle_enemy_balls.remove(ball)

            if respawn:
                list_two_turtle[0][10].clear()
                list_two_turtle[0][4] = list_two_turtle[0][2]
                list_two_turtle[0][5] = list_two_turtle[0][3]

                list_two_turtle[1][10].clear()
                list_two_turtle[1][4] = list_two_turtle[1][2]
                list_two_turtle[1][5] = list_two_turtle[1][3]
                respawn = False

            screen.blit(turtle_foto, turtle_rect)
    if not no_animation and not victory1 and not victory2:
        if counter - time >= 2000:
            no_animation = True
        for obstacle in list_of_obstacles:
            obstacle_archive = obstacle[0]
            obstacle_rect = obstacle[1]
            screen.blit(obstacle_archive, obstacle_rect)
        angle_turtle += 18
        turtle_p = pygame.transform.rotate(image, angle_turtle)
        turtle_animation_rect.center = (turtle_animation_x, turtle_animation_y)
        screen.blit(turtle_p, turtle_animation_rect)
        screen.blit(turtle_enemy_photo, turtle_enemy_rect)
    if list_two_turtle[1][11] <= 0:
        victory1 = True
    if list_two_turtle[0][11] <= 0:
        victory2 = True

    # draw hud
    hud1_text = font.render(str(list_two_turtle[0][11]), True, green)
    hud2_text = font.render(str(list_two_turtle[1][11]), True, red)
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
