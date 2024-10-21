import pygame
import random
import numpy as np

class SnakeGame:
    def __init__(self, width=440, height=440):
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.snake_dir = (10, 0)
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        return self.get_state()

    def spawn_food(self):
        return (random.randint(0, (self.width - 10) // 10) * 10,
                random.randint(0, (self.height - 10) // 10) * 10)

    def get_state(self):
        head_x, head_y = self.snake[0]
        food_x, food_y = self.food

        # Distance from food
        food_dist = (food_x - head_x, food_y - head_y)

        # Direction the snake is moving
        snake_dir = self.snake_dir

        # Snake body proximity
        body_collision = [0, 0, 0, 0]  # top, right, bottom, left

        for body_part in self.snake[1:]:
            if body_part == (head_x, head_y - 10):  # Up
                body_collision[0] = 1
            elif body_part == (head_x + 10, head_y):  # Right
                body_collision[1] = 1
            elif body_part == (head_x, head_y + 10):  # Down
                body_collision[2] = 1
            elif body_part == (head_x - 10, head_y):  # Left
                body_collision[3] = 1

        state = np.array(snake_dir + food_dist + tuple(body_collision))
        return state

    def step(self, action):
        directions = [(0, -10), (10, 0), (0, 10), (-10, 0)]
        self.snake_dir = directions[action]

        head_x, head_y = self.snake[0]
        new_head = (head_x + self.snake_dir[0], head_y + self.snake_dir[1])

        # Collision detection
        if (new_head in self.snake or
                new_head[0] < 0 or new_head[0] >= self.width or
                new_head[1] < 0 or new_head[1] >= self.height):
            self.game_over = True
            return self.get_state(), -10, True

        self.snake = [new_head] + self.snake[:-1]

        # Check if food is eaten
        if new_head == self.food:
            self.snake.append(self.snake[-1])
            self.food = self.spawn_food()
            self.score += 1
            reward = 10
        else:
            reward = 0

        return self.get_state(), reward, False

    def render(self, screen):
        screen.fill((0, 0, 0))
        for part in self.snake:
            pygame.draw.rect(screen, (0, 255, 0), (*part, 10, 10))
        pygame.draw.rect(screen, (255, 0, 0), (*self.food, 10, 10))
        pygame.display.update()
