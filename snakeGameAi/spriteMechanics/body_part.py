import pygame as pg
from . import settings
from .settings import vec
from .sprite_methods import remove_background_from_img

class BodyPart(pg.sprite.Sprite):
    def __init__(self, game, snake, x, y):
        self._layer = settings.BODY_LAYER
        self.groups = game.all_sprites, game.snake_body
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.rotate(self.game.snake_spritesheet.get_image(*settings.SNAKE_IMG_TAIL, settings.SIZE), 90)
        self.image = remove_background_from_img(self.image, settings.BLACK)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * settings.TILESIZE
        self.rect.topleft = self.pos

    def update(self):
        # Update rectangle
        self.rect.topleft = self.pos
