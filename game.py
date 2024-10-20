import sys
import random
import time
from collections import deque

import pygame

class Game:
    def __init__(self):
        self.GAME_OVER = 'GAME OVER'

        self.width, self.height = 800, 600

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.blue = (2, 128, 196)
        self.green = (12, 168, 22)
        self.snake = self.black

        self.x = self.width/2
        self.y = self.height/2

        self.block_size = 20

        self.score = 0
        self.clock_speed = 7

        pygame.init()

        self.display = pygame.display.set_mode((self.width, self.height))
        self.display.fill(self.white)
        pygame.display.update()
        pygame.display.set_caption('Snake Game')

        self.display_center = [(self.width/2)-100, (self.height/2)-50]

        self.clock = pygame.time.Clock()

    def start(self):
        self.game_loop()

        quit_game = False
        while not quit_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.exit()
                    elif event.key == pygame.K_c:
                        self.game_loop()

    def draw_snake(self, snake_path):
        for x, y in snake_path:
            pygame.draw.rect(self.display, self.snake, [x, y, self.block_size, self.block_size])

    def draw_food(self, food):
        pygame.draw.rect(self.display, self.red, [food[0], food[1], self.block_size, self.block_size])

    def generate_food(self):
        fx = round(random.randrange(0, self.width - self.block_size) / self.block_size) * self.block_size
        fy = round(random.randrange(0, self.height - self.block_size) / self.block_size) * self.block_size
        return [fx, fy]

    def game_loop(self):
        game_over = False
        self.reset_game()
        dx, dy = 0, 0

        food = self.generate_food()

        snake_path = deque()
        last_key = None
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN and not (last_key and last_key == pygame.K_UP):
                        last_key = pygame.K_DOWN
                        dx, dy = 0, dy + self.block_size
                    elif event.key == pygame.K_UP and not (last_key and last_key == pygame.K_DOWN):
                        last_key = pygame.K_UP
                        dx, dy = 0, dy - self.block_size
                    elif event.key == pygame.K_LEFT and not (last_key and last_key == pygame.K_RIGHT):
                        last_key = pygame.K_LEFT
                        dx, dy = dx - self.block_size, 0
                    elif event.key == pygame.K_RIGHT and not (last_key and last_key == pygame.K_LEFT):
                        last_key = pygame.K_RIGHT
                        dx, dy = dx + self.block_size, 0

            self.x += dx
            self.y += dy
            snake_head = (self.x, self.y)
            snake_path.append(snake_head)

            if self.x == food[0] and self.y == food[1]:
                self.score += 1
                food = self.generate_food()

            if len(snake_path) > self.score + 1:
                snake_path.popleft()

            self.display.fill(self.white)
            self.draw_snake(snake_path)
            self.draw_food(food)
            msg = f'Your Score: {self.score}'
            self.display_message(msg, self.black, [0, 10])
            pygame.display.update()

            for i  in range(len(snake_path)-1):
                block = snake_path[i]
                if block == snake_head:
                    game_over = True
                    time.sleep(1)
                    break

            if self.x < 0 or self.y < 0 or self.x >= self.width or self.y >= self.height:
                game_over = True

            self.clock.tick(self.clock_speed)

        self.display_game_over()

    def display_game_over(self):
        self.display.fill(self.white)
        msg = f'Your Score: {self.score}'
        self.display_message(msg, self.green, [self.display_center[0] + 20, self.display_center[1] - 100], 40)
        self.display_message(self.GAME_OVER, self.snake, self.display_center, 50)
        self.display_message('Press Q to Quit OR C to Play Again',
                             self.blue,
                             [self.display_center[0] - 55, self.display_center[1] + 50])
        pygame.display.update()

    def display_score(self, score):
        msg = f'Your Score: {score}'
        self.display_message(msg, self.black, [0, 0])


    def display_message(self, message, color, position=None, size=30):
        if position is None:
            position = [0, 0]
        font = pygame.font.SysFont(None, size)
        msg = font.render(message, True, color)
        self.display.blit(msg, position)

    def reset_game(self):
        self.x = self.width/2
        self.y = self.height/2
        self.score = 0

    def exit(self):
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    Game().start()


