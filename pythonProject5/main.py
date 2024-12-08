import pygame
import sys
import matplotlib.pyplot as plt
img_path = 'E:\4K\01 (1).jpg'
img = plt.imread(img_path)
plt.imshow(img)
plt.show()


# 初始化pygame
pygame.init()

# 设置窗口大小
screen = pygame.display.set_mode((480, 640))

# 加载资源
plane_img = pygame.image.load("01 (1).jpg")
bullet_img = pygame.image.load("01 (1).jpg")
enemy_img = pygame.image.load("01 (1).jpg")

# 初始化游戏参数
score = 0
life = 3

# 游戏循环
while True:
    # 处理游戏逻辑
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # 更新游戏画面
    screen.fill((255, 255, 255))
    screen.blit(plane_img, (200, 500))
    screen.blit(bullet_img, (200, 500))
    screen.blit(enemy_img, (200, 500))
    pygame.display.flip()

    # 监听用户输入
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        plane_img.rect.x -= 5
    if keys[pygame.K_RIGHT]:
        plane_img.rect.x += 5
    if keys[pygame.K_UP]:
        plane_img.rect.y -= 5
    if keys[pygame.K_DOWN]:
        plane_img.rect.y += 5

