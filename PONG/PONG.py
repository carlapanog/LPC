import turtle
import os
import vlc

# draw screen
screen = turtle.Screen()
screen.title("My Pong")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)


# draw paddle function
def draw_paddle(paddle, x, y):
    paddle.speed(0)
    paddle.shape("square")
    paddle.color("white")
    paddle.shapesize(stretch_wid=5, stretch_len=1)
    paddle.penup()
    paddle.goto(x, y)
    return paddle


# creating paddle 1 and paddle 2
paddle_1 = draw_paddle(turtle.Turtle(), -350, 0)
paddle_2 = draw_paddle(turtle.Turtle(), 350, 0)


# draw ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.2
ball.dy = -0.2

# score
score_1 = 0
score_2 = 0

# head-up display
hud = turtle.Turtle()
hud.speed(0)
hud.shape("square")
hud.color("white")
hud.penup()
hud.hideturtle()
hud.goto(0, 260)
hud.write("0 : 0", align="center", font=("Press Start 2P", 24, "normal"))


def paddle_up(paddle):
    y = paddle.ycor()
    if y < 250:
        y += 30
    else:
        y = 250
    return paddle.sety(y)


def paddle_down(paddle):
    y = paddle.ycor()
    if y > -250:
        y += -30
    else:
        y = -250
    return paddle.sety(y)


# keyboard
screen.listen()
screen.onkeypress(lambda n=paddle_1: paddle_up(n), "w")
screen.onkeypress(lambda n=paddle_1: paddle_down(n), "s")
screen.onkeypress(lambda n=paddle_2: paddle_up(n), "Up")
screen.onkeypress(lambda n=paddle_2: paddle_down(n), "Down")


while True:
    screen.update()

    # ball movement
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # collision with the upper wall
    if ball.ycor() > 290:
        vlc.MediaPlayer("bounce.wav")
        ball.sety(290)
        ball.dy *= -1

    # collision with lower wall
    if ball.ycor() < -290:
        vlc.MediaPlayer("bounce.wav")
        ball.sety(-290)
        ball.dy *= -1

    # collision with left wall
    if ball.xcor() < -390:
        score_2 += 1
        hud.clear()
        hud.write("{} : {}".format(score_1, score_2), align="center", font=("Press Start 2P", 24, "normal"))
        vlc.MediaPlayer("258020__kodack__arcade-bleep-sound.wav")
        ball.goto(0, 0)
        ball.dx *= -1

    # collision with right wall
    if ball.xcor() > 390:
        score_1 += 1
        hud.clear()
        hud.write("{} : {}".format(score_1, score_2), align="center", font=("Press Start 2P", 24, "normal"))
        vlc.MediaPlayer("258020__kodack__arcade-bleep-sound.wav")
        ball.goto(0, 0)
        ball.dx *= -1

    # collision with the paddle 1
    if (-350 < ball.xcor() < -340) and paddle_1.ycor() + 40 > ball.ycor() > paddle_1.ycor() - 40:
        ball.setx(-340)
        ball.dx *= -1
        vlc.MediaPlayer("bounce.wav")

    # collision with the paddle 2
    if (350 > ball.xcor() > 340) and paddle_2.ycor() + 40 > ball.ycor() > paddle_2.ycor() - 40:
        ball.setx(340)
        ball.dx *= -1
        vlc.MediaPlayer("bounce.wav")
