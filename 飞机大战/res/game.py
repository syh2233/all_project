import pygame
from game_item import *
from game_hud import *
from game_music import *


class Game(object):
    def __init__(self):
        self.main_window = pygame.display.set_mode(SCREEN_RECT.size)
        pygame.display.set_caption('飞机大战')
        self.is_game_over = False
        self.is_pause = False
        self.all_group = pygame.sprite.Group()
        self.enemies_group = pygame.sprite.Group()
        self.supplies_group = pygame.sprite.Group()
        GameSprite("", 1, self.all_group)
        hero = GameSprite("", 0, self.all_group)
        hero.rect.center = SCREEN_RECT.center


    def reset_game(self):
        self.is_game_over = False
        self.is_pause = False


    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                if self.is_game_over:
                    self.reset_game()
                else:
                    self.is_pause = not self.is_pause
        return False


    def start(self):
        clock = pygame.time.Clock()
        while True:
            if self.event_handler():
                return
            if self.is_game_over:
                print('游戏已经结束，按空格键重新开始...')
            elif self.is_pause:
                print('游戏已经暂停，按空格键继续...')
            else:
                print('游戏进行中...')
            self.all_group.draw(self.main_window)
            pygame.display.update()
            clock.tick(60)


if __name__ == '__main__':
    pygame.init()
    Game().start()
    pygame.quit()
