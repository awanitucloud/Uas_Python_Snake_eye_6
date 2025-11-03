# snake.py
import pygame
from config import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, GREEN, DARK_GREEN

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.score = 0
        for i in range(1, self.length):
            self.positions.append((self.positions[0][0] - i, self.positions[0][1]))

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        self.direction = point

    def move(self):
        head = self.get_head_position()
        x, y = self.direction
        new_position = ((head[0] + x) % GRID_WIDTH, (head[1] + y) % GRID_HEIGHT)
        if new_position in self.positions[1:]:
            return False
        self.positions.insert(0, new_position)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def draw(self, surface):
        for i, p in enumerate(self.positions):
            color = GREEN if i == 0 else (0, 200 - (i * 2) % 100, 0)
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, DARK_GREEN, rect, 1)

    def grow(self):
        self.length += 1
        self.score += 10
