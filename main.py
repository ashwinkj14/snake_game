import random
from collections import namedtuple
from enum import Enum

import pygame

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (2, 128, 196)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

Point = namedtuple('Point', 'x, y')

BLOCK_SIZE = 20

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

def exit_game():
    pygame.quit()

class Game:
    def __init__(self, w=640, h=480):
        self.snake = None
        self.w = w
        self.h = h

        self.score = 0
        self.speed = 5

        self.display = pygame.display.set_mode((self.w, self.h))
        self.display.fill(BLACK)
        pygame.display.update()
        pygame.display.set_caption('Snake Game')

        self.clock = pygame.time.Clock()

    def _reset(self):
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2)
        # Snake length is 3 blocks
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2*BLOCK_SIZE), self.head.y)]
        self.food = None
        self.score = 0

    def _spawn_food(self):
        while True:
            x = round(random.randrange(0, self.w - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            y = round(random.randrange(0, self.h - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            food = Point(x, y)
            if food not in self.snake:
                self.food = food
                return

    def _is_collision(self):
        # Condition to check if snake has bitten its body
        if self.head in self.snake[1:]:
            return True

        # Condition to check if snake has hit the wall
        if self.head.x < 0 or self.head.y < 0 or self.head.x >= self.w or self.head.y >= self.h:
            return True

        return False

    def _game_loop(self):
        play = True
        while True:
            if play:
                self._reset()
                self._play()
                self._game_over_screen()
                play = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return
                    elif event.key == pygame.K_c:
                        play = True

    def _update_frame(self):
        self.display.fill(BLACK)

        for point in self.snake:
            pygame.draw.rect(self.display, ORANGE, [point.x, point.y, BLOCK_SIZE, BLOCK_SIZE])
            pygame.draw.rect(self.display, YELLOW, [point.x+4, point.y+4, BLOCK_SIZE, BLOCK_SIZE])

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        self._display_message(f'Your Score : {self.score}', WHITE)
        pygame.display.update()
        pygame.display.flip()

    def _game_over_screen(self):
        self.display.fill(BLACK)
        center = Point(self.w / 2, self.h / 2)

        msg = f'Your Score: {self.score}'
        self._display_message(msg, GREEN, [5, 5])

        self._display_message('GAME OVER', RED, [center.x - 100, center.y - 50], 50)

        self._display_message('Press Q to Quit OR C to Play Again',
                             LIGHTBLUE,
                             [center.x + 20 - (self.w / 4), center.y])
        pygame.display.update()

    def _display_message(self, message, color, position=None, size=25):
        if position is None:
            position = [0, 0]
        font = pygame.font.SysFont(None, size)
        msg = font.render(message, True, color)
        self.display.blit(msg, position)

    def _move(self, direction):
        dx, dy = 0, 0
        match direction:
            case Direction.RIGHT:
                nx = -BLOCK_SIZE
                if self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                    nx = BLOCK_SIZE
                dx += nx
            case Direction.LEFT:
                nx = BLOCK_SIZE
                if self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                    nx = -BLOCK_SIZE
                dx += nx
            case Direction.UP:
                ny = BLOCK_SIZE
                if self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                    ny = -BLOCK_SIZE
                dy += ny
            case Direction.DOWN:
                ny = -BLOCK_SIZE
                if self.direction != Direction.UP:
                    self.direction = Direction.DOWN
                    ny = BLOCK_SIZE
                dy += ny

        self.head = Point(self.head.x + dx, self.head.y + dy)

    def _play(self):
        self._spawn_food()
        direction = self.direction
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        direction = Direction.DOWN
                    elif event.key == pygame.K_UP:
                        direction = Direction.UP
                    elif event.key == pygame.K_LEFT:
                        direction = Direction.LEFT
                    elif event.key == pygame.K_RIGHT:
                        direction = Direction.RIGHT

            self._move(direction)
            self.snake.insert(0, self.head)

            if self._is_collision():
                return

            if self.head == self.food:
                self.score += 1
                self._spawn_food()
            else:
                self.snake.pop()

            self._update_frame()

            self.clock.tick(self.speed)

    def start(self):
        self._game_loop()
        exit_game()


if __name__ == '__main__':
    Game().start()


