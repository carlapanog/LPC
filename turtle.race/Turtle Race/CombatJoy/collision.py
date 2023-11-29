import pygame.time

pygame.init()


def collide_with_wall(turtle_or_ball, pos_x, pos_y, w, h, bt):

    side_right = pos_x + w
    side_left = pos_x
    side_up = pos_y
    side_down = pos_y + h
    if bt == 0:
        turtle_x = turtle_or_ball.get_current_x()
        turtle_y = turtle_or_ball.get_current_y()
        speed_x = turtle_or_ball.get_speed()[0]
        speed_y = turtle_or_ball.get_speed()[1]
    else:
        turtle_x = turtle_or_ball.get_x_pos()
        turtle_y = turtle_or_ball.get_y_pos()
        speed_x = turtle_or_ball.get_speed_x()
        speed_y = turtle_or_ball.get_speed_y()

    if (
            (turtle_x > side_right and side_up < turtle_y < side_down) or
            (turtle_x > side_right and (abs(turtle_x - side_right) > abs(turtle_y - side_up))) or
            (turtle_x > side_right and (abs(turtle_x - side_right) > abs(turtle_y - side_down)))
    ):

        turtle_x += abs(speed_x)

        if bt == 1:
            speed_x *= -1

    if (
            (side_left < turtle_x < side_right and turtle_y > side_down) or
            (turtle_y > side_down and (abs(turtle_y - side_down) > abs(turtle_x - side_right))) or
            (turtle_y > side_down and (abs(turtle_y - side_down) > abs(turtle_x - side_left)))
    ):

        turtle_y += abs(speed_y)

        if bt == 1:
            speed_y *= -1

    if (
            (turtle_x < side_left and side_up < turtle_y < side_down) or
            (turtle_x < side_left and (abs(turtle_x - side_left) > abs(turtle_y - side_up))) or
            (turtle_x < side_left and (abs(turtle_x - side_left) > abs(turtle_y - side_down)))
    ):

        turtle_x += -(abs(speed_x))

        if bt == 1:
            speed_x *= -1

    if (
            (side_left < turtle_x < side_right and turtle_y < side_up) or
            (turtle_y < side_up) and (abs(turtle_y - side_up > abs(turtle_x - side_left))) or
            (turtle_y < side_up) and (abs(turtle_y - side_up > abs(turtle_x - side_right)))
    ):

        turtle_y += -(abs(speed_y))

        if bt == 1:
            speed_y *= -1

    pos = [turtle_x, turtle_y]
    speed = [speed_x, speed_y]
    pos_speed = (pos, speed)
    return pos_speed
