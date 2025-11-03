# game.py
import pygame
import sys
from config import *
from snake import Snake
from food import Food

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Game Ular Klasik")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 20)
        self.big_font = pygame.font.SysFont('Arial', 40)
        self.snake = Snake()
        self.food = Food()
        self.high_score = 0
        self.game_over = False
        self.level = 1
        self.speed = FPS

    def update_level(self):
        self.level = self.snake.score // 50 + 1
        self.speed = FPS + (self.level - 1) * 2

    def draw_grid(self):
        for x in range(0, WIDTH, GRID_SIZE):
            for y in range(0, HEIGHT, GRID_SIZE):
                rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(self.screen, GRAY, rect, 1)

    def draw_score(self):
        score_text = self.font.render(f'Skor: {self.snake.score}', True, WHITE)
        high_score_text = self.font.render(f'Skor Tertinggi: {self.high_score}', True, WHITE)
        level_text = self.font.render(f'Level: {self.level}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_score_text, (WIDTH - high_score_text.get_width() - 10, 10))
        self.screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 10))

    def draw_game_over(self):
        game_over_text = self.big_font.render('GAME OVER', True, RED)
        restart_text = self.font.render('Tekan SPACE untuk melanjutkan', True, WHITE)
        self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))

    def check_win(self):
        return self.snake.length == GRID_WIDTH * GRID_HEIGHT

    def draw_win(self):
        win_text = self.big_font.render('ANDA MENANG!', True, GREEN)
        restart_text = self.font.render('Tekan SPACE untuk bermain lagi', True, WHITE)
        self.screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 50))
        self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if self.game_over and event.key == pygame.K_SPACE:
                        self.snake.reset()
                        self.food.randomize_position()
                        self.game_over = False
                        self.level = 1
                        self.speed = FPS
                    elif event.key == pygame.K_UP:
                        self.snake.turn(UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.turn(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.turn(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.turn(RIGHT)

            if not self.game_over:
                if not self.snake.move():
                    self.game_over = True
                    if self.snake.score > self.high_score:
                        self.high_score = self.snake.score

                if self.snake.get_head_position() == self.food.position:
                    self.snake.grow()
                    self.food.randomize_position()
                    while self.food.position in self.snake.positions:
                        self.food.randomize_position()
                    self.update_level()

                if self.check_win():
                    self.game_over = True
                    if self.snake.score > self.high_score:
                        self.high_score = self.snake.score

            self.screen.fill(BLACK)
            self.draw_grid()
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            self.draw_score()

            if self.game_over:
                if self.check_win():
                    self.draw_win()
                else:
                    self.draw_game_over()

            pygame.display.update()
            self.clock.tick(self.speed)
