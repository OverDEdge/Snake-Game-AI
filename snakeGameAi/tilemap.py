import pygame as pg
from . import settings

class Map:

    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * settings.TILESIZE
        self.height = self.tileheight * settings.TILESIZE
