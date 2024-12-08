import pygame
import sys
import random

# 初始化pygame
pygame.init()

# 设置窗口大小和标题
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('贪吃蛇')

# 定义颜色
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
# 初始化蛇和食物的位置
snake_pos = [[100, 100], [80, 100], [60, 100]]
food_pos = [300, 300]

# 初始化蛇的移动方向
move_direction = 'right'

# 游戏主循环
while True:
    # 处理游戏事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and move_direction != 'down':
                move_direction = 'up'
            elif event.key == pygame.K_DOWN and move_direction != 'up':
                move_direction = 'down'
            elif event.key == pygame.K_LEFT and move_direction != 'right':
                move_direction = 'left'
            elif event.key == pygame.K_RIGHT and move_direction != 'left':
                move_direction = 'right'

    # 更新蛇的位置
    if move_direction == 'up':
        new_pos = [snake_pos[0][0], snake_pos[0][1] - 20]
    elif move_direction == 'down':
        new_pos = [snake_pos[0][0], snake_pos[0][1] + 20]
    elif move_direction == 'left':
        new_pos = [snake_pos[0][0] - 20, snake_pos[0][1]]
    else:
        new_pos = [snake_pos[0][0] + 20, snake_pos[0][1]]

    snake_pos.insert(0, new_pos)
    if new_pos == food_pos:
        food_pos = [random.randrange(1, 32) * 20, random.randrange(1, 24) * 20]
    else:
        snake_pos.pop()

    # 检测蛇是否撞到自己或者边界
    if (new_pos[0] < 0 or new_pos[0] >= 640 or new_pos[1] < 0 or new_pos[1] >= 480 or new_pos in snake_pos[1:]):
        pygame.quit()
        sys.exit()

    # 绘制游戏画面
    screen.fill(WHITE)
    for pos in snake_pos:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], 20, 20))
    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], 20, 20))
    pygame.display.flip()

    # 控制游戏速度
    pygame.time.Clock().tick(10)
