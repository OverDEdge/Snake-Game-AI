# Snake game created by Niklas Moberg

import pygame as pg
import sys
from os import path
import random
from .food import Food
from .body_part import BodyPart
from .ground import Ground
from .snake import Snake
from .spritesheet import Spritesheet
from .wall import Wall
from .tilemap import Map
from . import settings
from . import gen_map

class Game:
    def __init__(self):
        # Intialize game window, etc...
        self.running_program = True
        pg.init()
        gen_map.generate_map()
        pg.mixer.init()
        self.screen = pg.display.set_mode((settings.WIDTH + 1, settings.HEIGHT + 1))
        pg.display.set_caption(settings.TITLE)
        self.clock = pg.time.Clock()
        self.map = Map(path.join(settings.MAP_FOLDER, settings.MAP_IMG))
        self.font_name = pg.font.match_font(settings.FONT_NAME)
        self.snake_spritesheet = Spritesheet(path.join(settings.IMG_FOLDER, settings.SNAKE_SPRITESHEET))
        self.load_data()

    def load_data(self):
        # Load Highscore file
        with open(path.join(settings.GAME_FOLDER, settings.HIGHSCORE_FILE), 'a+') as f:
            f.seek(0)
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0


    def new(self):
        self.load_data()
        # Setup for a new game
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.snake_body = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.LayeredUpdates()
        self.ground = pg.sprite.LayeredUpdates()
        self.food = pg.sprite.LayeredUpdates()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                #Ground(self, col, row)
                if tile == '1':
                    self.spawn_wall(col, row)
                if tile == 'S':
                    self.snake = Snake(self, col, row)

        Food(self)
        self.run()

    def spawn_wall(self, x ,y):
        Wall(self, x, y)

    def update(self):
        # Game Loop - update
        self.all_sprites.update()
        if self.snake.collide:
            self.playing = False

    def draw_grid(self):
        x = 0
        y = 0

        # Vertical lines
        for _ in range(settings.GRIDWIDTH + 1):
            pg.draw.line(self.screen, settings.WHITE, (x, 0), (x, settings.HEIGHT))
            x += settings.TILESIZE

        # Horizontal lines
        for _ in range(settings.GRIDHEIGHT + 1):
            pg.draw.line(self.screen, settings.WHITE, (0, y), (settings.WIDTH, y))
            y += settings.TILESIZE


    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(settings.FPS) / 1000.0
            self.events()
            self.update()
            self.draw()

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def draw(self):
        # Game Loop - draw
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(settings.BGCOLOR)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.pos)
        #self.draw_grid()
        self.draw_text(str(self.score), 25, settings.WHITE, settings.WIDTH / 2, 5)
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def launch_go_screen(self):
        # Game Over screen

        if self.score > self.highscore:
            with open(path.join(settings.GAME_FOLDER, settings.HIGHSCORE_FILE), 'w') as f:
                self.highscore = self.score
                f.write(str(self.score))
            self.draw_text(settings.NEW_HIGHSCORE_TEXT + str(self.score), 30, settings.RED, settings.WIDTH / 2, settings.HEIGHT * 2 / 3)
        else:
            self.draw_text(settings.SCORE_TEXT + str(self.score), 25, settings.YELLOW, settings.WIDTH / 2, settings.HEIGHT * 3 / 4)
            self.draw_text(settings.HIGH_SCORE_TEXT + str(self.highscore), 30, settings.RED, settings.WIDTH / 2, settings.HEIGHT * 3 / 5)

        self.draw_text(settings.GAME_OVER_TEXT, 40, settings.WHITE, settings.WIDTH / 2, settings.HEIGHT / 4)
        self.draw_text(settings.PRESS_TO_PLAY_AGAIN, 17, settings.YELLOW, settings.WIDTH / 2, settings.HEIGHT * 2 / 5)
        pg.display.flip()
        self.wait_for_key()

    def launch_start_screen(self):
        # Start screen
        self.screen.fill(settings.BGCOLOR)
        self.draw_text(settings.TITLE, 60, settings.YELLOW, settings.WIDTH / 2, settings.HEIGHT / 3)
        self.draw_text(settings.PRESS_TO_PLAY, 20, settings.GREEN, settings.WIDTH / 2, settings.HEIGHT * 3 / 5)
        self.draw_text(settings.HIGH_SCORE_TEXT + str(self.highscore), 25, settings.RED, settings.WIDTH / 2, settings.HEIGHT * 1 / 6)
        pg.display.flip()
        self.wait_for_key()

    # Waiting for any key input
    def wait_for_key(self):
        waiting = True
        key_down = False
        while waiting:
            self.clock.tick(settings.FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.quit()
                if event.type == pg.KEYDOWN:
                    key_down = True
                if event.type == pg.KEYUP and key_down:
                    waiting = False

    def quit(self):
        pg.quit()
        sys.exit()

g = Game()

while g.running_program:
    g.launch_start_screen()
    g.new()
    g.launch_go_screen()

pg.quit()
sys.exit()
