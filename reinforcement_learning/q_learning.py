import pickle
from collections import defaultdict
import random

from reinforcement_learning.snake_game import SnakeGame
import matplotlib.pyplot as plt

class QLearning:
    def __init__(self):
        self.actions = ((1,0,0), (0,1,0), (0,0,1))
        self.q_table = defaultdict(lambda: {a: 0.0 for a in self.actions})

    def load_q_table(self):
        with open("q_table.pkl", "rb") as f:
            self.q_table = pickle.load(f)

    def select_action(self, state, epsilon=0.1):
        if random.random() < epsilon:
            return random.choice(self.actions)
        return max(self.q_table[state], key=self.q_table[state].get)

    def update_q_table(self, state, action, reward, next_state, alpha=0.005, gamma=0.9):
        old_value = self.q_table[state][action]
        next_max = max(self.q_table[next_state].values()) if next_state in self.q_table else 0.0

        # Bellman update
        new_value = old_value + alpha * (reward + gamma * next_max - old_value)
        self.q_table[state][action] = new_value

    def train(self):
        game = SnakeGame()
        epsilon = 0.1
        scores = []
        for episode in range(10000):
            game.reset()
            state = game.get_state()
            done = False

            while not done:
                action = self.select_action(state, epsilon)
                next_state, reward, done = game.step(action)
                next_state = game.get_state()

                self.update_q_table(state, action, reward, next_state)
                state = next_state

            epsilon = max(0.01, epsilon * 0.995)
            scores.append(game.score)
            if episode % 100 == 0:
                print(f'CURRENT EPISODE: {episode}, AVG SCORE: {sum(scores[-100:])/100}')
        print(f'MAX SCORE : {max(scores)}')
        plt.plot(scores, label='Scores')
        plt.show(block=True)

        with open("q_table.pkl", "wb") as f:
            pickle.dump(dict(self.q_table), f)

    def test(self):
        self.load_q_table()
        game = SnakeGame(render=True)

        epsilon = 0.1
        for i in range(10):
            game.reset()
            state = game.get_state()
            done = False
            while not done:
                action = self.select_action(state, epsilon)
                state, reward, done = game.step(action)

            print(f'SCORE: {game.score}')
