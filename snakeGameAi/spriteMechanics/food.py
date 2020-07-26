import pygame as pg
import random
from os import path
from . import settings
from .settings import vec
from .sprite_methods import check_for_collision, remove_background_from_img

class Food(pg.sprite.Sprite):
    def __init__(self, game, index):
        self._layer = settings.FOOD_LAYER
        self.game = game
        self.groups = game.all_sprites, game.food_groups[index]
        self.index = index
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.transform.scale(pg.image.load(path.join(settings.IMG_FOLDER, settings.FOOD_IMG)).convert(), settings.SIZE)
        self.image = remove_background_from_img(self.image, settings.BLACK)
        self.rect = self.image.get_rect()
        self.place_food()
        self.pos_update_time = 0

    def place_food(self):
        '''
        Places food at a random location, checking that a sprite doesn't already
        exist there.
        '''
        self.col = random.randrange(settings.GRIDWIDTH - 1)
        self.row = random.randrange(settings.GRIDHEIGHT - 1)
        self.pos = vec(self.col, self.row)
        self.rect.topleft = self.pos * settings.TILESIZE
        if check_for_collision(self, self.game.walls, False) or check_for_collision(self, self.game.snake_body_groups[self.index], False):
            self.place_food()

    def update(self):
        pass
