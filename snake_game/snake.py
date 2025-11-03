# snake.py
import pygame
import os
from config import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT

class Snake:
    def __init__(self):
        self.reset()
        self.load_assets()

    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.score = 0
        for i in range(1, self.length):
            self.positions.append((self.positions[0][0] - i, self.positions[0][1]))

    def load_assets(self):
        base_path = os.path.join(os.path.dirname(__file__), "assets")

        self.head_imgs = {
            'up': pygame.image.load(os.path.join(base_path, "head_up.png")).convert_alpha(),
            'down': pygame.image.load(os.path.join(base_path, "head_down.png")).convert_alpha(),
            'left': pygame.image.load(os.path.join(base_path, "head_left.png")).convert_alpha(),
            'right': pygame.image.load(os.path.join(base_path, "head_right.png")).convert_alpha()
        }

        self.body_imgs = {
            'vertical': pygame.image.load(os.path.join(base_path, "body_vertical.png")).convert_alpha(),
            'horizontal': pygame.image.load(os.path.join(base_path, "body_horizontal.png")).convert_alpha(),
            'topleft': pygame.image.load(os.path.join(base_path, "body_topleft.png")).convert_alpha(),
            'topright': pygame.image.load(os.path.join(base_path, "body_topright.png")).convert_alpha(),
            'bottomleft': pygame.image.load(os.path.join(base_path, "body_bottomleft.png")).convert_alpha(),
            'bottomright': pygame.image.load(os.path.join(base_path, "body_bottomright.png")).convert_alpha()
        }

        self.tail_imgs = {
            'up': pygame.image.load(os.path.join(base_path, "tail_up.png")).convert_alpha(),
            'down': pygame.image.load(os.path.join(base_path, "tail_down.png")).convert_alpha(),
            'left': pygame.image.load(os.path.join(base_path, "tail_left.png")).convert_alpha(),
            'right': pygame.image.load(os.path.join(base_path, "tail_right.png")).convert_alpha()
        }

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
            rect = pygame.Rect(p[0] * GRID_SIZE, p[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)

            if i == 0:
                direction = self.get_direction_name(self.direction)
                head_img = self.head_imgs.get(direction, self.head_imgs['right'])
                surface.blit(pygame.transform.scale(head_img, (GRID_SIZE, GRID_SIZE)), rect)
            elif i == len(self.positions) - 1:
                tail_dir = self.get_tail_direction()
                tail_img = self.tail_imgs.get(tail_dir, self.tail_imgs['right'])
                surface.blit(pygame.transform.scale(tail_img, (GRID_SIZE, GRID_SIZE)), rect)
            else:
                body_type = self.get_body_type(i)
                body_img = self.body_imgs.get(body_type, self.body_imgs['horizontal'])
                surface.blit(pygame.transform.scale(body_img, (GRID_SIZE, GRID_SIZE)), rect)

    def grow(self):
        self.length += 1
        self.score += 10

    def get_direction_name(self, direction):
        if direction == (0, -1): return 'up'
        if direction == (0, 1): return 'down'
        if direction == (-1, 0): return 'left'
        if direction == (1, 0): return 'right'
        return 'right'  # ✅ fallback default

    def get_tail_direction(self):
        if len(self.positions) < 2:
            return 'right'  # ✅ fallback jika terlalu pendek
        tail = self.positions[-1]
        before_tail = self.positions[-2]
        dx = tail[0] - before_tail[0]
        dy = tail[1] - before_tail[1]
        return self.get_direction_name((dx, dy))

    def get_body_type(self, i):
        prev = self.positions[i - 1]
        curr = self.positions[i]
        next = self.positions[i + 1]

        dx1 = curr[0] - prev[0]
        dy1 = curr[1] - prev[1]
        dx2 = next[0] - curr[0]
        dy2 = next[1] - curr[1]

        if dx1 == dx2:
            return 'horizontal'
        elif dy1 == dy2:
            return 'vertical'
        elif (dx1, dy2) == (-1, -1) or (dx2, dy1) == (-1, -1):
            return 'bottomright'
        elif (dx1, dy2) == (1, -1) or (dx2, dy1) == (1, -1):
            return 'bottomleft'
        elif (dx1, dy2) == (-1, 1) or (dx2, dy1) == (-1, 1):
            return 'topright'
        elif (dx1, dy2) == (1, 1) or (dx2, dy1) == (1, 1):
            return 'topleft'
        return 'horizontal'  # ✅ fallback default
