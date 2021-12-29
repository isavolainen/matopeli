#-------------------------------------------------------------------------------
# Module       matopeli
# Author:      Ilja Savolainen
# Created:     29.12.2021
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import random
import pygame

# Settings
TITLE = "Snape"
VERSION = 1.0
DIFFICULTY = 8
FONT = "Consolas"
(SCREEN_X, SCREEN_Y) = (800, 800)
FPS = 60
MARGIN = 20
BORDER = 10
EDGE = MARGIN + BORDER
COLOR = (255, 180, 180)
BG_COLOR = (100, 20, 0)

# Class definitions
class Snake:

    def __init__(self, pos=(SCREEN_X//2, SCREEN_Y//2)):
        """Create and initialize a Snake instance at target position."""
        self.heading = "right"
        self.speed = 4
        self.length = 32
        self.size = 16
        self.color = COLOR
        self.pos = pos
        (self.x_coord, self.y_coord) = ([], [])
        self.displacement = 0
        for _ in range(self.length):
            self.x_coord.append(self.pos[0] - self.displacement)
            self.y_coord.append(self.pos[1])
            self.displacement += 4

    def turn(self, direction):
        if direction == "right" and self.heading != "left":
            self.heading = "right"
        elif direction == "left" and self.heading != "right":
            self.heading = "left"
        elif direction == "up" and self.heading != "down":
            self.heading = "up"
        elif direction == "down" and self.heading != "up":
            self.heading = "down"

    def move(self):
        # Moving the head
        if self.heading == "right":
            self.x_coord[0] += self.speed
        elif self.heading == "left":
            self.x_coord[0] -= self.speed
        elif self.heading == "up":
            self.y_coord[0] -= self.speed
        elif self.heading == "down":
            self.y_coord[0] += self.speed
        # Moving the rest
        for i in range(self.length - 1, 0, -1):
            self.x_coord[i] = self.x_coord[i - 1]
            self.y_coord[i] = self.y_coord[i - 1]

    def grow(self):
        for _ in range(DIFFICULTY):
            self.length += 1
            self.x_coord.append(self.x_coord[-1])
            self.y_coord.append(self.y_coord[-1])

    def draw(self, surface):
        for i in range(self.length):
            draw_area = (self.x_coord[i], self.y_coord[i], self.size, self.size)
            surface.fill(self.color, draw_area)

    def collision(self):
        """Checks if the snake has collided with a wall or with itself."""
        # Check collision with walls
        (x_coord, y_coord) = (self.x_coord[0], self.y_coord[0])
        if x_coord <= EDGE or x_coord >= SCREEN_X - self.size - EDGE or \
            y_coord <= EDGE or y_coord >= SCREEN_Y - self.size - EDGE:
            return True
        # Check collision with self
        corners = self.get_corners()
        if self.heading == "right":
            (frontleft_x, frontleft_y) = (corners[1][0], corners[1][1])
            (frontright_x, frontright_y) = (corners[2][0], corners[2][1])
        elif self.heading == "left":
            (frontleft_x, frontleft_y) = (corners[3][0], corners[3][1])
            (frontright_x, frontright_y) = (corners[0][0], corners[0][1])
        elif self.heading == "up":
            (frontleft_x, frontleft_y) = (corners[0][0], corners[0][1])
            (frontright_x, frontright_y) = (corners[1][0], corners[1][1])
        elif self.heading == "down":
            (frontleft_x, frontleft_y) = (corners[2][0], corners[2][1])
            (frontright_x, frontright_y) = (corners[3][0], corners[3][1])
        for i in range(len(self.x_coord)):
            if self.x_coord[i] < frontleft_x < self.x_coord[i] + self.size and \
                self.y_coord[i] < frontleft_y < self.y_coord[i] + self.size:
                return True
            if self.x_coord[i] < frontright_x < self.x_coord[i] + self.size and \
                self.y_coord[i] < frontright_y < self.y_coord[i] + self.size:
                return True
        return False

    def get_corners(self):
        """Returns the coordinates for all corners of the snake's head."""
        (x_coord, y_coord) = (self.x_coord[0], self.y_coord[0])
        corner0 = (x_coord, y_coord)
        corner1 = (x_coord + self.size, y_coord)
        corner2 = (x_coord + self.size, y_coord + self.size)
        corner3 = (x_coord, y_coord + self.size)
        return (corner0, corner1, corner2, corner3)

class Food:
    def __init__(self):
        """Create and initialize a Food instance at a random location."""
        self.size = 16
        self.color = COLOR
        self.pos = self.spawn()

    def spawn(self):
        """Spawn in a random location."""
        (x_coord, y_coord) = (0, 0)
        grid_x = SCREEN_X // self.size
        grid_y = SCREEN_Y // self.size
        while x_coord < EDGE + 5 or x_coord > SCREEN_X - self.size - EDGE - 5:
            x_coord = random.randrange(grid_x) * self.size
        while y_coord < EDGE + 5 or y_coord > SCREEN_Y - self.size - EDGE - 5:
            y_coord = random.randrange(grid_y) * self.size
        return (x_coord, y_coord)

    def draw(self, surface):
        draw_area = (self.pos[0], self.pos[1], self.size, self.size)
        surface.fill(self.color, draw_area)


# Function definitions
def draw_endscreen(surface):
    surface.fill(BG_COLOR)
    game_over_1 = font_xl.render("YOU DIED", True, (COLOR))
    game_over_2 = font_l.render(f"Score: {score}", True, (COLOR))
    game_over_3 = font_l.render("Do you want to play again? y/n", True, (COLOR))
    rect_1 = game_over_1.get_rect(center = (SCREEN_X // 2, SCREEN_Y // 2))
    rect_1 = (rect_1[0], rect_1[1] - SCREEN_Y // 8)
    rect_2 = game_over_2.get_rect(center = (SCREEN_X // 2, SCREEN_Y // 2))
    rect_2 = (rect_2[0], rect_2[1])
    rect_3 = game_over_3.get_rect(center = (SCREEN_X // 2, SCREEN_Y // 2))
    rect_3 = (rect_3[0], rect_3[1] + SCREEN_Y // 12)
    surface.blit(game_over_1, rect_1)
    surface.blit(game_over_2, rect_2)
    surface.blit(game_over_3, rect_3)

def collides(snake_object, food_object):
    """Checks if the snake has collided with food."""
    snake_corners = snake_object.get_corners()
    (food_x, food_y) = food_object.pos
    for coord in snake_corners:
        if food_x <= coord[0] <= food_x + food_object.size and \
            food_y <= coord[1] <= food_y + food_object.size:
            return True
    return False


if __name__ == "__main__":
    # Main loop
    while True:
        # Game setup
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
        pygame.display.set_caption(f'{TITLE} {VERSION}')
        font_xl = pygame.font.SysFont(FONT, 96)
        font_l = pygame.font.SysFont(FONT, 24)
        font_m = pygame.font.SysFont(FONT, 18)
        snake = Snake()
        food = Food()
        score = 0
        game_state = 1
        frame_count = 0
        seconds = 0

        # Game loop
        while game_state == 1:
            # Event handling
            for event in pygame.event.get():
#                if event.type == pygame.KEYDOWN:
#                    print(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        snake.turn("left")
                    if event.key == pygame.K_RIGHT:
                        snake.turn("right")
                    if event.key == pygame.K_UP:
                        snake.turn("up")
                    if event.key == pygame.K_DOWN:
                        snake.turn("down")
                    if event.key == pygame.K_ESCAPE:
                        game_state = -1
                        break
                if event.type == pygame.QUIT:
                    game_state = -1
                    break

            # Gameplay
            snake.move()
            if collides(snake, food):
                score += 10
                snake.grow()
                del food
                food = Food()
            if snake.collision():
                game_state = 0

            # Draw calls
            screen.fill(BG_COLOR)
            screen.fill(COLOR, (MARGIN, MARGIN, SCREEN_X - 2 * MARGIN, SCREEN_Y - 2 * MARGIN))
            screen.fill(BG_COLOR, (EDGE, EDGE, SCREEN_X - 2 * EDGE, SCREEN_Y - 2 * EDGE))
            the_score = font_l.render(f"Score: {score}", True, COLOR)
            screen.blit(the_score, (EDGE + 10, EDGE + 10))
            time = font_l.render(f"Time: {seconds}", True, COLOR)
            screen.blit(time, (SCREEN_X - 150, EDGE + 10))
            snake.draw(screen)
            food.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
            frame_count += 1
            if frame_count % 60 == 0:
                seconds += 1

        # End loop
        while game_state == 0:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_state = -1
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_n:
                        game_state = -1
                    if event.key == pygame.K_y:
                        game_state = 1

            # Draw calls
            draw_endscreen(screen)
            pygame.display.flip()
            clock.tick(FPS)

        if game_state < 1:
            break

    pygame.quit()
