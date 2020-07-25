import pygame as pg
import random
from os import path
from . import settings
from .settings import vec
from .sprite_methods import check_for_collision, remove_background_from_img

class Food(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = settings.FOOD_LAYER
        self.game = game
        self.groups = game.all_sprites, game.food
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
        self.pos = vec(random.randrange(settings.GRIDWIDTH - 1), random.randrange(settings.GRIDHEIGHT - 1)) * settings.TILESIZE
        self.rect.topleft = self.pos
        if check_for_collision(self, self.game.walls, False) or check_for_collision(self, self.game.snake_body, False):
            self.place_food()

    def update(self):
        now = pg.time.get_ticks()

        if (now - self.pos_update_time) > settings.FOOD_POS_UPDATE_RATE:
            self.get_new_position()
            self.pos_update_time = now

    def get_new_position(self):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        dir = random.choice(directions)
        self.pos.x += dir[0] * settings.TILESIZE
        self.pos.y += dir[1] * settings.TILESIZE
        self.rect.topleft = self.pos
        if check_for_collision(self, self.game.walls, False) or check_for_collision(self, self.game.snake_body, False):
            self.pos.x -= dir[0] * settings.TILESIZE
            self.pos.y -= dir[1] * settings.TILESIZE
            self.get_new_position()
