import pygame as pg
from os import path
from . import settings
from .settings import vec
from .sprite_methods import check_for_collision, remove_background_from_img, animate_moving, load_moving_images
from .body_part import BodyPart
from .food import Food

class Snake(pg.sprite.Sprite):
    def __init__(self, game, col, row, food, index):
        '''
        Initializing Snake head
        '''
        self._layer = settings.SNAKE_LAYER
        self.groups = game.all_sprites
        self.index = index
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.food = food
        self.pos = vec(col, row)
        self.prev_pos = vec(self.pos.x, self.pos.y)
        self.vel = vec(1, 0)
        self.body_parts = [BodyPart(self.game, self, col - 1, row, self.index)]
        self.images = []
        self.colorkey = settings.WHITE
        load_moving_images(self, self.game.snake_spritesheet, settings.SNAKE_IMG_HEAD, self.colorkey)
        self.image_id = 0
        self.non_rot_image = self.images[self.image_id]
        self.image = self.non_rot_image
        self.non_rot_tail = self.game.snake_spritesheet.get_image(*settings.SNAKE_IMG_TAIL, settings.SIZE)
        self.tail = self.non_rot_tail
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos * settings.TILESIZE
        self.pos_update_time = 0
        self.collide = False
        self.key = 'none'
        self.dir = 'right'
        self.prev_dir = self.dir
        self.last_change_img_time = 0
        self.img_upd_time = settings.SWITCH_SPRITE_IMAGE
        self.update_rate = settings.SNAKE_LEVEL1_UPDATE_RATE
        self.grid_position = [[0] * (settings.GRIDHEIGHT) for _ in range(settings.GRIDWIDTH)]
        self.max_moves = settings.MAX_MOVES
        self.moves = 0

        # Key mappings
        self.inputState = {
                'up': False,
                'down': False,
                'right': False,
                'left': False,
                'none': False
        }

    def update(self):
        # Get current time
        now = pg.time.get_ticks()

        # Only update position at certain intervals (if display is active)
        # SNAKE_UPDATE_RATE determines snake speed
        if self.game.display:
            #if now - self.pos_update_time > self.update_rate:
            self.update_ai_output()
            self.move_in_direction()
            animate_moving(self, self.images)
            self.update_ai_collisions()
        else:
            self.update_ai_output()
            self.move_in_direction()
            self.update_ai_collisions()

    def update_ai_dist_to_object(self, group):
        '''
        Method for AI to know distances to a group in eight directions
        '''
        # Save current position
        current_pos = vec(self.pos.x, self.pos.y)

        directions = [vec(1, 0), vec(-1, 0), vec(1, 1), vec(-1, 1), vec(0, 1), vec(0, -1), vec(1, -1), vec(-1, -1)]
        distances = [0] * len(directions)

        for i, dir in enumerate(directions):
            self.pos = vec(current_pos.x, current_pos.y)

            # Check how far until collide with object in current direction
            while not check_for_collision(self, group, False) and 0 <= self.pos.x <= settings.GRIDWIDTH and 0 <= self.pos.y <= settings.GRIDHEIGHT:
                self.pos += dir
                self.rect.topleft = self.pos * settings.TILESIZE

            # After collision calculate the distance
            distances[i] = math.sqrt((current_pos.x - self.pos.x) ** 2 + (current_pos.y - self.pos.y) ** 2)

        # Reset position
        self.pos = current_pos
        self.rect.topleft = self.pos * settings.TILESIZE

        return distances

    def update_ai_output(self):
        '''
        Method for AI to calculate output and action
        '''
        # Get distance to next object
        distances_wall = self.update_ai_dist_to_object(self.game.walls)
        distances_body = self.update_ai_dist_to_object(self.game.snake_body_groups[self.index])
        distances_food = self.update_ai_dist_to_object(self.game.food_groups[self.index])

        output = self.game.nets[self.index].activate(
                (*distances_wall, *distances_body, *distances_food)
        )

        # Reset move
        self.inputState = {
                'up': False,
                'down': False,
                'right': False,
                'left': False,
                'none': False
        }

        # Interpret ai ouput to move
        if output[0] == max(output):
            self.inputState['left'] = True
        elif output[1] == max(output):
            self.inputState['right'] = True
        elif output[2] == max(output):
            self.inputState['up'] = True
        else:
            self.inputState['down'] = True

        self.moves += 1

    def update_ai_collisions(self):
        '''
        Method to check if AI has collided with anything
        '''
        # To avoid circling, keep track of how many times a position has been visted
        self.grid_position[int(self.pos.x)][int(self.pos.y)] += 1

        if check_for_collision(self, self.game.snake_body_groups[self.index], False) or check_for_collision(self, self.game.walls, False) or self.moves > self.max_moves:
            self.game.collided_snake(self)
        else:
            self.game.ge[self.index].fitness += 0.1
            self.update_positions()
            self.update_eat_food()

    def update_eat_food(self):
        '''
        Check if snake has found food and if yes adds another body part
        '''
        # Check if snake eats food
        if check_for_collision(self, self.game.food, True):
            self.game.score += 10
            last_body_part = self.body_parts[-1]
            self.body_parts.append(BodyPart(self.game, self, last_body_part.pos.x, last_body_part.pos.y))
            Food(self.game)

    def update_positions(self):
        self.update_body_parts_positions()

        # Update snake head position
        self.pos += self.vel * settings.TILESIZE
        self.pos_update_time = pg.time.get_ticks()

        self.update_body_parts_img()
        self.update_head_img()
        self.update_tail_img()

        #self.update_screen_wrap()

        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

    def update_body_parts_positions(self):
        '''
        Loops through the body parts and updates the positions
        Necessary to do in Snake object to get synced updates
        '''
        for i in range(len(self.body_parts) - 1, 0, -1):
            self.body_parts[i].pos = self.body_parts[i - 1].pos

        self.body_parts[0].pos = vec(self.pos.x, self.pos.y)

    def update_head_img(self):

        if self.dir == 'up':
            self.image = pg.transform.flip(self.non_rot_image, False, True)
        if self.dir == 'right':
            self.image = pg.transform.rotate(self.non_rot_image, 90)
        if self.dir == 'left':
            self.image = pg.transform.rotate(self.non_rot_image, -90)
        if self.dir == 'down':
            self.image = self.non_rot_image

    def update_body_parts_img(self):
        '''
        Sets the appropriate body image depending on position
        '''

        # Behind head
        if len(self.body_parts) > 1:
            self.body_parts[0].image = self.update_correct_body_part(self.body_parts[1].pos, self.body_parts[0].pos, self.pos)
            self.body_parts[0].image = remove_background_from_img(self.body_parts[0].image, self.colorkey)

        # Rest of body
        for i in range(1, len(self.body_parts) - 1):
            self.body_parts[i].image = self.update_correct_body_part(self.body_parts[i + 1].pos, self.body_parts[i].pos, self.body_parts[i - 1].pos)
            self.body_parts[i].image = remove_background_from_img(self.body_parts[i].image, self.colorkey)

    def update_tail_img(self):
        '''
        Set appropriate image for tail
        '''

        tail_pos = self.body_parts[-1].pos

        if len(self.body_parts) > 1:
            front_of_tail = self.body_parts[-2].pos
        else:
            front_of_tail = self.pos

        if front_of_tail.y < tail_pos.y:
            self.body_parts[-1].image = self.non_rot_tail
        if front_of_tail.x > tail_pos.x:
            self.body_parts[-1].image = pg.transform.rotate(self.non_rot_tail, 90)
        if front_of_tail.y > tail_pos.y:
            self.body_parts[-1].image = pg.transform.flip(self.non_rot_tail, False, True)
        if front_of_tail.x < tail_pos.x:
            self.body_parts[-1].image = pg.transform.rotate(self.non_rot_tail, -90)

        self.body_parts[-1].image = remove_background_from_img(self.body_parts[-1].image, self.colorkey)

    def update_correct_body_part(self, pos_pre, pos, pos_post):
        if pos_pre.x == pos_post.x:
            return self.game.snake_spritesheet.get_image(*settings.SNAKE_IMG_BODY, settings.SIZE)
        if pos_pre.y == pos_post.y:
            return pg.transform.rotate(self.game.snake_spritesheet.get_image(*settings.SNAKE_IMG_BODY, settings.SIZE), 90)
        if (pos.x < pos_post.x and pos_pre.y < pos.y or
            pos_pre.x > pos.x and pos.y > pos_post.y):
            return self.game.snake_spritesheet.get_image(*settings.SNAKE_IMG_TURN[0], settings.SIZE)
        if (pos.x < pos_post.x and pos_pre.y > pos.y or
            pos_pre.x > pos.x and pos.y < pos_post.y):
            return self.game.snake_spritesheet.get_image(*settings.SNAKE_IMG_TURN[1], settings.SIZE)
        if (pos.x > pos_post.x and pos.y < pos_pre.y or
            pos_pre.x < pos.x and pos.y < pos_post.y):
            return self.game.snake_spritesheet.get_image(*settings.SNAKE_IMG_TURN[2], settings.SIZE)
        if (pos.x > pos_post.x and pos.y > pos_pre.y or
            pos_pre.x < pos.x and pos.y > pos_post.y):
            return self.game.snake_spritesheet.get_image(*settings.SNAKE_IMG_TURN[3], settings.SIZE)

    def update_screen_wrap(self):
        '''
        Wraps snake position from edge of screen to other side
        '''
        if self.pos.x > settings.WIDTH - settings.TILESIZE:
            self.pos.x = 0
        elif self.pos.x < 0:
            self.pos.x = settings.WIDTH - settings.TILESIZE
        if self.pos.y > settings.HEIGHT - settings.TILESIZE:
            self.pos.y = 0
        elif self.pos.y < 0:
            self.pos.y = settings.HEIGHT - settings.TILESIZE

    def move_pressed_key(self):
        '''
        Gets the key inputs and sets the correct binding
        '''
        keys = pg.key.get_pressed()
        for binding, keysBound in settings.MOVE_BINDINGS.items():
            for key in keysBound:
                if keys[key]:
                    self.inputState[binding] = True
                    break
                else:
                    self.inputState[binding] = False

    def move_is_key_pressed(self):
        '''
        Removes bindings when key is no longer pressed
        '''
        if not self.inputState[self.key]:
            self.key = 'none'

    def move_in_direction(self):
        '''
        Loops over all directions and sets velocity based on user input
        '''
        directions = ('left', 'right', 'up', 'down')
        vel = (vec(-1, 0), vec(1, 0), vec(0, -1), vec(0, 1))
        vel_check = (-self.vel.x, self.vel.x, -self.vel.y, self.vel.y)

        for i, dir in enumerate(directions):
            if self.inputState[dir] and vel_check[i] >= 0:
                if self.key == 'none':
                    self.vel = vel[i]
                    self.dir = dir
                    self.key = dir

        # To get smooth game feel give user reaction immediatly when turning
        if self.prev_dir != self.dir:
            self.pos_update_time = 0
            self.prev_dir = self.dir
