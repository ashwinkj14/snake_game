import random
from collections import namedtuple
from enum import Enum
import pygame

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

class SnakeGame:
    def __init__(self, render=False, w=640, h=480):
        self.render = render
        self.snake = None
        self.w = w
        self.h = h

        self.score = 0
        self.speed = 5

    def reset(self):
        if self.render:
            pygame.init()
            self.display = pygame.display.set_mode((self.w, self.h))
            self.display.fill(BLACK)
            pygame.display.update()
            pygame.display.set_caption('Snake Game')

            self.clock = pygame.time.Clock()

        self.direction = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2)
        # Snake length is 3 blocks
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2*BLOCK_SIZE), self.head.y)]
        self.food = None
        self.score = 0
        self.steps_without_food = 0
        self._spawn_food()

    def _spawn_food(self):
        while True:
            x = round(random.randrange(0, self.w - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            y = round(random.randrange(0, self.h - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            food = Point(x, y)
            if food not in self.snake:
                self.food = food
                return

    def get_state(self):
        pt_l = Point(self.head.x - BLOCK_SIZE, self.head.y)
        pt_r = Point(self.head.x + BLOCK_SIZE, self.head.y)
        pt_u = Point(self.head.x, self.head.y - BLOCK_SIZE)
        pt_d = Point(self.head.x, self.head.y + BLOCK_SIZE)

        direction_l = self.direction == Direction.LEFT
        direction_r = self.direction == Direction.RIGHT
        direction_u = self.direction == Direction.UP
        direction_d = self.direction == Direction.DOWN

        obstacles = [
            # Straight
            (direction_l and self._is_collision(pt_l)) or
            (direction_r and self._is_collision(pt_r)) or
            (direction_u and self._is_collision(pt_u)) or
            (direction_d and self._is_collision(pt_d)),

            # Right
            (direction_l and self._is_collision(pt_u)) or
            (direction_r and self._is_collision(pt_d)) or
            (direction_u and self._is_collision(pt_r)) or
            (direction_d and self._is_collision(pt_l)),

            # Left
            (direction_l and self._is_collision(pt_d)) or
            (direction_r and self._is_collision(pt_u)) or
            (direction_u and self._is_collision(pt_l)) or
            (direction_d and self._is_collision(pt_r))
        ]

        direction = [direction_r, direction_d, direction_l, direction_u]

        food_location = [
            self.head.x < self.food.x,# RIGHT
            self.head.y < self.food.y,# DOWN
            self.head.x > self.food.x,# LEFT
            self.head.y > self.food.y # UP
        ]

        state = food_location + obstacles + direction
        return tuple(state)

    def _snake_is_collision(self, point):
        # Condition to check if snake has bitten its body
        if point in self.snake[1:]:
            return True
        return False

    def _edge_is_collision(self, point):
        # Condition to check if snake has hit the wall
        if point.x < 0 or point.y < 0 or point.x >= self.w or point.y >= self.h:
            return True

        return False

    def _is_collision(self, point):
        # Condition to check if snake has bitten its body
        if point in self.snake[1:]:
            return True

        # Condition to check if snake has hit the wall
        if point.x < 0 or point.y < 0 or point.x >= self.w or point.y >= self.h:
            return True

        return False

    def _update_frame(self):
        self.display.fill(BLACK)

        for point in self.snake:
            pygame.draw.rect(self.display, ORANGE, [point.x, point.y, BLOCK_SIZE, BLOCK_SIZE])
            pygame.draw.rect(self.display, YELLOW, [point.x+4, point.y+4, BLOCK_SIZE, BLOCK_SIZE])

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        self._display_message(f'Your Score : {self.score}', WHITE)
        pygame.display.update()
        pygame.display.flip()

    def _display_message(self, message, color, position=None, size=25):
        if position is None:
            position = [0, 0]
        font = pygame.font.SysFont(None, size)
        msg = font.render(message, True, color)
        self.display.blit(msg, position)

    def _move(self, action):
        directions = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = directions.index(self.direction)

        new_direction = self.direction
        if action == (0, 1, 0):# RIGHT TURN
            new_direction = directions[(idx + 1) % len(directions)]
        elif action == (0, 0, 1):# LEFT TURN
            new_direction = directions[(idx - 1) % len(directions)]

        dx, dy = 0, 0
        match new_direction:
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

    def step(self, action):
        self._move(action)
        self.snake.insert(0, self.head)

        if self._is_collision(self.head):
            exit_game()
            return self.get_state(), -100, True

        reward = 0
        if self.head == self.food:
            self.score += 1
            self._spawn_food()
            reward = 10
            self.steps_without_food = 0
        else:
            self.steps_without_food += 1
            reward = -0.1
            self.snake.pop()

        if self.steps_without_food > 200:
            exit_game()
            return self.get_state(), -10, True

        if self.render:
            self._update_frame()
            self.clock.tick(self.speed)

        return self.get_state(), reward, False
