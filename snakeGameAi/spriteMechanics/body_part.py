import pygame as pg
from . import settings
from .settings import vec
from .sprite_methods import remove_background_from_img

class BodyPart(pg.sprite.Sprite):
    def __init__(self, game, snake, col, row, index):
        self._layer = settings.BODY_LAYER
        self.groups = game.all_sprites, game.snake_body_groups[index]
        pg.sprite.Sprite.__init__(self, self.groups)
        self.index = index
        self.game = game
        self.image = pg.transform.rotate(self.game.snake_spritesheet.get_image(*settings.SNAKE_IMG_TAIL, settings.SIZE), 90)
        self.image = remove_background_from_img(self.image, settings.WHITE)

        self.rect = self.image.get_rect()
        self.pos = vec(int(col), int(row))
        self.rect.topleft = self.pos * settings.TILESIZE

    def update(self):
        # Update rectangle
        self.rect.topleft = self.pos * settings.TILESIZE
