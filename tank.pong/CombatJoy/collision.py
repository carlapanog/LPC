import pygame.time

pygame.init()


def collide_with_wall(tank_or_ball, pos_x, pos_y, w, h, bt):

    side_right = pos_x + w
    side_left = pos_x
    side_up = pos_y
    side_down = pos_y + h
    if bt == 0:
        tank_x = tank_or_ball.get_current_x()
        tank_y = tank_or_ball.get_current_y()
        speed_x = tank_or_ball.get_speed()[0]
        speed_y = tank_or_ball.get_speed()[1]
    else:
        tank_x = tank_or_ball.get_x_pos()
        tank_y = tank_or_ball.get_y_pos()
        speed_x = tank_or_ball.get_speed_x()
        speed_y = tank_or_ball.get_speed_y()

    if (
            (tank_x > side_right and side_up < tank_y < side_down) or
            (tank_x > side_right and (abs(tank_x - side_right) > abs(tank_y - side_up))) or
            (tank_x > side_right and (abs(tank_x - side_right) > abs(tank_y - side_down)))
    ):

        tank_x += abs(speed_x)

        if bt == 1:
            speed_x *= -1

    if (
            (side_left < tank_x < side_right and tank_y > side_down) or
            (tank_y > side_down and (abs(tank_y - side_down) > abs(tank_x - side_right))) or
            (tank_y > side_down and (abs(tank_y - side_down) > abs(tank_x - side_left)))
    ):

        tank_y += abs(speed_y)

        if bt == 1:
            speed_y *= -1

    if (
            (tank_x < side_left and side_up < tank_y < side_down) or
            (tank_x < side_left and (abs(tank_x - side_left) > abs(tank_y - side_up))) or
            (tank_x < side_left and (abs(tank_x - side_left) > abs(tank_y - side_down)))
    ):

        tank_x += -(abs(speed_x))

        if bt == 1:
            speed_x *= -1

    if (
            (side_left < tank_x < side_right and tank_y < side_up) or
            (tank_y < side_up) and (abs(tank_y - side_up > abs(tank_x - side_left))) or
            (tank_y < side_up) and (abs(tank_y - side_up > abs(tank_x - side_right)))
    ):

        tank_y += -(abs(speed_y))

        if bt == 1:
            speed_y *= -1

    pos = [tank_x, tank_y]
    speed = [speed_x, speed_y]
    pos_speed = (pos, speed)
    return pos_speed
