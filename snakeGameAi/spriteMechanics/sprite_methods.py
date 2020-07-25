import pygame as pg
import random
from os import path
from . import settings

def check_for_collision(sprite, group, remove):
    '''
    Checks for collision between a sprite and a group
    '''
    hits = pg.sprite.spritecollide(sprite, group, remove)
    if hits:
        return True

def remove_background_from_img(image, colorkey):
    '''
    Removes background from image
    '''

    image.set_colorkey(colorkey)
    image.convert_alpha()

    return image

# Animate movement for a sprite
def animate_moving(sprite, image_array):
    now = pg.time.get_ticks()
    if (now - sprite.last_change_img_time) > sprite.img_upd_time:
        sprite.image_id += 1

        if sprite.image_id >= len(image_array):
            sprite.image_id = 0

        image = image_array[sprite.image_id]

        sprite.last_change_img_time = now
        sprite.non_rot_image = image

def load_moving_images(sprite, spritesheet, image_coordinates, colorkey):
    for location in image_coordinates:
        image = spritesheet.get_image(*location, settings.SIZE)
        image = remove_background_from_img(image, colorkey)
        sprite.images.append(image)
