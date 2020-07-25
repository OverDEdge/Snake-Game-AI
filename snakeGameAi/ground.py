import pygame as pg
from . import settings
from .settings import vec
from .sprite_methods import remove_background_from_img

class Ground(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # Add to sprites group
        self._layer = settings.GROUND_LAYER
        self.groups = game.all_sprites, game.ground
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface(settings.SIZE)
        self.image.fill(settings.BGCOLOR)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * settings.TILESIZE
        self.rect.topleft = self.pos
