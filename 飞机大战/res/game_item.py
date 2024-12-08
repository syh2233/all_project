import pygame

SCREEN_RECT = pygame.Rect(0, 0, 480, 700)

class GameSprite(pygame.sprite.Sprite):
    res_path = "./res/images/"
    def __init__(self, image_name, speed, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(self.res_path + image_name)
        self.rect = self.image.get_rect()
        self.speed = speed
    def update(self, *args):
        self.rect.y += self.speed

