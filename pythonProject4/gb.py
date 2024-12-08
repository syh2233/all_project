from turtle import *


def square(x, y, size, color_name):
    up()
    goto(x, y)
    down()
    color (color_name)
    begin_fill()

    forward(size)
    left(90)
    forward(size)
    left(90)
    forward(size)
    left(90)
    forward(size)
    left(90)

    end_fill()


# setup(420, 420, 0, 0)
# hideturtle()
# tracer(False)
# square(50, 50, 10, "red")
# done()
