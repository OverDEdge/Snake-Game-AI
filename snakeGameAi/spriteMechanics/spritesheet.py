import pygame as pg
from . import settings

class Spritesheet:
    # Utility class for loading and parsing spritessheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height, size):
        # Grab an image out of a larger Spreadsheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (int(size[0]), int(size[1])))
        return image
