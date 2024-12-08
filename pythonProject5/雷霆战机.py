from turtle import *
from gamebasic import square
from random import randrange

plane = [[0, -120], [10, -120], [20, -120], [10, -110]]
apple_x = randrange(-20, 18) * 10
apple_y = randrange(0, 19) * 10
apple_x1 = randrange(-20, 18) * 10
apple_y1 = randrange(0, 19) * 10
apple_x2 = randrange(-20, 18) * 10
apple_y2 = randrange(0, 19) * 10
enemy =[[apple_x,apple_y],[apple_x+10,apple_y],[apple_x+20,apple_y],[apple_x+10,apple_y-10],[apple_x1,apple_y1],[apple_x1+10,apple_y1],[apple_x1+20,apple_y1],[apple_x1+10,apple_y1-10],[apple_x2,apple_y2],[apple_x2+10,apple_y2],[apple_x2+20,apple_y2],[apple_x2+10,apple_y2-10],]
enemyzidan =[[apple_x+10,apple_y-20],[apple_x+10,apple_y-30]]
enemyzidan1 =[[apple_x1+10,apple_y1-20],[apple_x1+10,apple_y1-30]]
enemyzidan2 =[[apple_x2+10,apple_y2-20],[apple_x2+10,apple_y2-30]]
planezidan=[[plane[3][0],plane[3][1]+10],[plane[3][0],plane[3][1]]]
aim_x = 0
aim_y = -10
aim_x1 = 0
aim_y1 = 10
aim_x2 = 0
aim_y2 = 0

def change(x, y):
    global aim_x2, aim_y2
    aim_x2 = x
    aim_y2 = y
def gameLoop():
    global apple_x, apple_y,enemy,plane,aim_x ,aim_y,aim_x1,aim_y1
    enemyzidan.append([enemyzidan[-1][0] + aim_x, enemyzidan[-1][1] + aim_y])
    enemyzidan.pop(0)
    enemyzidan1.append([enemyzidan1[-1][0] + aim_x, enemyzidan1[-1][1] + aim_y])
    enemyzidan1.pop(0)
    enemyzidan2.append([enemyzidan2[-1][0] + aim_x, enemyzidan2[-1][1] + aim_y])
    enemyzidan2.pop(0)
    planezidan.append([planezidan[-1][0] + aim_x1, planezidan[-1][1] + aim_y1])
    planezidan.pop(0)
    clear()
    for n in range(len(enemyzidan)):
        square(enemyzidan[0][0], enemyzidan[1][1], 10, "red")
    for n in range(len(enemyzidan1)):
        square(enemyzidan1[0][0], enemyzidan1[1][1], 10, "red")
    for n in range(len(enemyzidan2)):
        square(enemyzidan2[0][0], enemyzidan2[1][1], 10, "red")
    for n in range(len(planezidan)):
        square(planezidan[0][0], planezidan[1][1], 10, "black")

    for n in range(len(enemy)):
        square(enemy[n][0], enemy[n][1], 10, "red")
    for n in range(len(plane)):
        square(plane[n][0]+aim_x2, plane[n][1]+aim_y2, 10, "black")
    ontimer(gameLoop, 300)
    update()

setup(420, 420, 0, 0)
hideturtle()
tracer(False)
gameLoop()
listen()
onkey(lambda: change(0, aim_y2+10), "w")
onkey(lambda: change(0, aim_y2-10), "s")
onkey(lambda: change(aim_x2-10, 0), "a")
onkey(lambda: change(aim_x2+10, 0), "d")
done()
