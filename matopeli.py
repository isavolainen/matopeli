#-------------------------------------------------------------------------------
# Module       matopeli
# Author:      Ilja Savolainen
# Created:     01.02.2018
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import pygame
import random
import time

SCREEN_X = 800
SCREEN_Y = 800
FPS = 60
MARGIN = 20
BORDER = 10
BG_COLOR = (100,20,0)
COLOR = (255,255,255)
BORDER_COLOR = COLOR
TEXT_COLOR = COLOR
SNAKE_COLOR = COLOR
FOOD_COLOR = COLOR

SPEED = 4
SNAKE_SIZE = 16
FOOD_SIZE = SNAKE_SIZE
(UP, RIGHT, DOWN, LEFT) = (0, 1, 2, 3)

KEY_ESC = 27
KEY_N = 110
KEY_T = 116
KEY_Y = 121
KEY_UP = 273
KEY_DOWN = 274
KEY_RIGHT = 275
KEY_LEFT = 276

arrow_keys = (KEY_UP, KEY_DOWN, KEY_RIGHT, KEY_LEFT)
perimeter = MARGIN + BORDER
mid = (SCREEN_X//2, SCREEN_Y//2)
grid = (SCREEN_X//FOOD_SIZE, SCREEN_Y//FOOD_SIZE)


# Class definitions
class Snake:

    heading = RIGHT
    speed = SPEED
    color = SNAKE_COLOR
    length = 20


    def __init__(self, size=SNAKE_SIZE, pos=mid):
        """ Create and initialize a Snake instance of target size at
            target position.
        """
        self.size = size
        self.pos = pos
        print(self.pos)
        self.x = []
        self.y = []
        for i in range(self.length):
            self.x.append(self.pos[0])
            self.y.append(self.pos[1])
        #print(self.x)
        #print(self.y)

    def update(self):
        """ Update the position of all sections. """
        if self.heading == UP:
            self.y[0] -= self.speed
        elif self.heading == RIGHT:
            self.x[0] += self.speed
        elif self.heading == DOWN:
            self.y[0] += self.speed
        elif self.heading == LEFT:
            self.x[0] -= self.speed
        #print(self.x[0], self.y[0])

        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

    def turn(self, key):
        if key == KEY_UP and self.heading != DOWN:
            self.heading = UP
        elif key == KEY_RIGHT and self.heading != LEFT:
            self.heading = RIGHT
        elif key == KEY_DOWN and self.heading != UP:
            self.heading = DOWN
        elif key == KEY_LEFT and self.heading != RIGHT:
            self.heading = LEFT

    def grow(self):
        self.length += 1
        self.x.append(self.x[-1])
        self.y.append(self.y[-1])

    def draw(self, surface):
        for i in range(self.length):
            draw_area = (self.x[i], self.y[i], self.size, self.size)
            surface.fill(self.color, draw_area)

##    def collision(self): # Bounce from walls
##        (x, y) = self.pos
##        if x <= perimeter:
##            self.pos = (x+1, y)
##            self.vx = -self.vx
##        if x >= SCREEN_X-self.size-perimeter:
##            self.pos = (x-1, y)
##            self.vx = -self.vx
##        if y < perimeter:
##            self.pos = (x, y+1)
##            self.vy = -self.vy
##        if y >= SCREEN_Y-self.size-perimeter:
##            self.pos = (x, y-1)
##            self.vy = -self.vy

    def collision(self):
        # Check collision with walls
        (x, y) = (self.x[0], self.y[0])
        if x <= perimeter or x >= SCREEN_X-self.size-perimeter or \
           y <= perimeter or y >= SCREEN_Y-self.size-perimeter:
            return True

        # Check collision with self

        return False

    def get_corners(self):
        (x, y) = (self.x[0], self.y[0])
        a = (x, y)
        b = (x+self.size, y)
        c = (x+self.size, y+self.size)
        d = (x, y+self.size)
        return (a, b, c, d)


class Food:

    def __init__(self, size=FOOD_SIZE, color=FOOD_COLOR):
        """ Create and initialize a Food object at a random position. """
        self.size = size
        self.color = color
        self.pos = self.spawn()

    def spawn(self):
        """ Returns a random location (x, y) on the playing area. """
        (x, y) = (0, 0)
        grid_x = SCREEN_X // self.size
        grid_y = SCREEN_Y // self.size
        while x < perimeter+5 or x > SCREEN_X-self.size-perimeter-5:
            x = random.randrange(grid_x) * self.size
        while y < perimeter+5 or y > SCREEN_Y-self.size-perimeter-5:
            y = random.randrange(grid_y) * self.size
        return (x, y)

    def draw(self, surface):
        (x, y) = self.pos
        draw_area = (x, y, self.size, self.size)
        surface.fill(self.color, draw_area)


# Function definitions
def draw_border(surface):
    (width, margin) = (BORDER, MARGIN)
    length_x = SCREEN_X-2*margin
    length_y = SCREEN_Y-2*margin
    color = BORDER_COLOR
    b_left = (margin, margin, width, length_y)
    b_right = (SCREEN_X-perimeter, margin, width, length_y)
    b_top = (margin, margin, length_x, width)
    b_bottom = (margin, SCREEN_Y-perimeter, length_x, width)
    surface.fill(color, b_left)
    surface.fill(color, b_right)
    surface.fill(color, b_top)
    surface.fill(color, b_bottom)


def draw_endscreen(surface):
    surface.fill(BG_COLOR)
    game_over_1 = font_xl.render("YOU DIED", True, (TEXT_COLOR))
    game_over_2 = font_l.render("Score: {0}".format(score),
            True, (TEXT_COLOR))
    game_over_3 = font_l.render("Do you want to play again? y/n",
            True, (TEXT_COLOR))
    rect_1 = game_over_1.get_rect(center=mid)
    rect_1 = (rect_1[0], rect_1[1]-SCREEN_Y//8)
    rect_2 = game_over_2.get_rect(center=mid)
    rect_2 = (rect_2[0], rect_2[1])
    rect_3 = game_over_3.get_rect(center=mid)
    rect_3 = (rect_3[0], rect_3[1]+SCREEN_Y//12)
    surface.blit(game_over_1, rect_1)
    surface.blit(game_over_2, rect_2)
    surface.blit(game_over_3, rect_3)


def collides(snake, food):
    s_corners = snake.get_corners()
    (f_x, f_y) = food.pos
    for coord in s_corners:
        (x, y) = coord
        if f_x <= x <= f_x+food.size and f_y <= y <= f_y+food.size:
            return True
    return False

# main():
while True:
    """ Main loop """

    # Game setup
    pygame.init()
    clock = pygame.time.Clock()
    surface = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    pygame.display.set_caption('Snape v0.1')
    pygame.mixer.init(48000, -16, 2, 2048)
    font_xl = pygame.font.SysFont("Consolas", 64)
    font_l = pygame.font.SysFont("Consolas", 24)
    font_m = pygame.font.SysFont("Consolas", 18)
    font_s = pygame.font.SysFont("Consolas", 14)
    try:
        death_sound = pygame.mixer.Sound("you_died.ogg")
        death_sound.set_volume(0.5)
    except:
        pass
    snake = Snake()
    food = Food()
    score = 0
    game_state = 1

    # FPS
    frame_count = 0
    frame_rate = 0
    draw_stats = 0
    t0 = time.clock()

    while game_state == 1:
        """ Game loop """

        # Event handling
        ev = pygame.event.poll()
        if ev.type != pygame.NOEVENT and ev.type != pygame.MOUSEMOTION and\
                ev.type != pygame.KEYUP:
            print(ev)
        if ev.type == pygame.QUIT:
            game_state = -1
            break
        if ev.type == pygame.KEYDOWN:
            key = ev.dict["key"]
            if key == KEY_ESC:
                game_state = -1
                break
            if key == KEY_T:
                if draw_stats == 0:
                    draw_stats = 1
                else:
                    draw_stats = 0
            if key in arrow_keys:
                snake.turn(key)

        # FPS
        frame_count += 1
        if frame_count % 30 == 0:
            t1 = time.clock()
            frame_rate = 30 / (t1-t0)
            t0 = t1

        #if frame_count % 4 == 0:
        snake.update()
        if collides(snake, food):
            score += 1
            snake.grow()
            del food
            food = Food()

        # Draw calls
        surface.fill(BG_COLOR)
        draw_border(surface)
        the_score = font_m.render("Score: {0}"
                .format(score), True, (255,255,255))
        surface.blit(the_score, (perimeter+10, perimeter+10))
        if draw_stats == 1:
            frame_text = font_s.render("Frame: {0}"
                    .format(frame_count), True, (TEXT_COLOR))
            fps_text = font_s.render("FPS: {0:.2f}"
                    .format(frame_rate), True, (TEXT_COLOR))
            surface.blit(frame_text, (perimeter+10, SCREEN_Y-perimeter-50))
            surface.blit(fps_text, (perimeter+10, SCREEN_Y-perimeter-30))
        snake.draw(surface)
        food.draw(surface)
        pygame.display.flip()
        clock.tick(FPS)
        if snake.collision():
            game_state = 0
            #death_sound.play()

    while game_state == 0:
        """ End loop """

        # Event handling
        ev = pygame.event.poll()
        if ev.type != pygame.NOEVENT and ev.type != pygame.MOUSEMOTION and \
                ev.type != pygame.KEYUP:
            print(ev)
        if ev.type == pygame.QUIT:
            break
        if ev.type == pygame.KEYDOWN:
            key = ev.dict["key"]
            if key == KEY_ESC or key == KEY_N:
                break
            if key == KEY_Y:
                game_state = 1
                snake = Snake()

        # Draw calls
        draw_endscreen(surface)
        pygame.display.flip()
        clock.tick(FPS)

    if game_state < 1:
        break

pygame.quit()
