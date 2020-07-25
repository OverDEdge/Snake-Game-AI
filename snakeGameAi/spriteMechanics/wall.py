import pygame as pg
from . import settings
from os import path
from .settings import vec
from .sprite_methods import remove_background_from_img

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # Add to sprites group
        self._layer = settings.WALL_LAYER
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.scale(pg.image.load(path.join(settings.IMG_FOLDER, settings.WALL_IMG)).convert(), settings.SIZE)
        self.image = remove_background_from_img(self.image, settings.BLACK)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * settings.TILESIZE
        self.rect.topleft = self.pos
