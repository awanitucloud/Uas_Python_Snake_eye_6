# food.py
import pygame
import random
import os
from config import GRID_WIDTH, GRID_HEIGHT, GRID_SIZE

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.load_image()
        self.randomize_position()

    def load_image(self):
        base_path = os.path.join(os.path.dirname(__file__), "assets")
        self.image = pygame.image.load(os.path.join(base_path, "food.png")).convert_alpha()

    def randomize_position(self):
        self.position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1)
        )

    def draw(self, surface):
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE
        )
        surface.blit(pygame.transform.smoothscale(self.image, (GRID_SIZE, GRID_SIZE)), rect)
