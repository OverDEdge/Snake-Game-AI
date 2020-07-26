import pygame as pg
from os import path

# Create vector
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
LIGHTPURPLE = (177, 156, 217)

# AI Settings
NUMBER_OF_GENOMES = 100
MAX_MOVES = 100
EXTRA_MOVES = 100

# Game settings
TILESIZE = 32
GRIDWIDTH = 22
GRIDHEIGHT = 17
WIDTH = GRIDWIDTH * TILESIZE   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = GRIDHEIGHT * TILESIZE  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Snake Game AI"
BGCOLOR = BLACK
HIGHSCORE_FILE = 'highscore.txt'

# Folder settings
GAME_FOLDER = path.dirname(__file__)
IMG_FOLDER = path.join(GAME_FOLDER, 'img')
MAP_FOLDER = path.join(GAME_FOLDER, 'maps')

# Text Prompts
FONT_NAME = 'arial'

# Snake settings
SNAKE_START_UPDATE_RATE = 120
SNAKE_START_POS = (2, 2)

# Food settings
FOOD_POS_UPDATE_RATE = 1000

# Layers
SNAKE_LAYER = 3
BODY_LAYER = 2
WALL_LAYER = 2
FOOD_LAYER = 2
GROUND_LAYER = 1

# Move
MOVE_BINDINGS = {
        'up': {pg.K_UP, pg.K_w},
        'down': {pg.K_DOWN, pg.K_s},
        'left': {pg.K_LEFT, pg.K_a},
        'right': {pg.K_RIGHT, pg.K_d}
}

# Graphics
SNAKE_SPRITESHEET = 'Snake2.png'
FOOD_IMG = 'food.png'
WALL_IMG = 'leavesBlock.png'
GROUND_IMG = 'Ground.png'
MAP_IMG = 'level1.txt'
SWITCH_SPRITE_IMAGE = 200
SIZE = (TILESIZE - 1, TILESIZE - 1)
SNAKE_IMG_SIZE = 42
SNAKE_IMG_HEAD = []
SNAKE_IMG_TURN = []

for i in range(3):
    SNAKE_IMG_HEAD.append((0, i * SNAKE_IMG_SIZE, SNAKE_IMG_SIZE, SNAKE_IMG_SIZE))

SNAKE_IMG_TAIL = (SNAKE_IMG_SIZE, 2 * SNAKE_IMG_SIZE, SNAKE_IMG_SIZE, SNAKE_IMG_SIZE)
SNAKE_IMG_BODY = (2 * SNAKE_IMG_SIZE, 2 * SNAKE_IMG_SIZE, SNAKE_IMG_SIZE, SNAKE_IMG_SIZE)

SNAKE_IMG_TURN.append((SNAKE_IMG_SIZE, SNAKE_IMG_SIZE, SNAKE_IMG_SIZE, SNAKE_IMG_SIZE))
SNAKE_IMG_TURN.append((SNAKE_IMG_SIZE, 0, SNAKE_IMG_SIZE, SNAKE_IMG_SIZE))
SNAKE_IMG_TURN.append((2 * SNAKE_IMG_SIZE, 0, SNAKE_IMG_SIZE, SNAKE_IMG_SIZE))
SNAKE_IMG_TURN.append((2 * SNAKE_IMG_SIZE, SNAKE_IMG_SIZE, SNAKE_IMG_SIZE, SNAKE_IMG_SIZE))
