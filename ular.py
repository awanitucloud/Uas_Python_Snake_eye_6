import pygame
import random
import sys

# Inisialisasi Pygame
pygame.init()

# Konstanta
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10  # Kecepatan game (tidak terlalu cepat)

# Warna
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 100, 0)
GRAY = (40, 40, 40)

# Arah
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.score = 0
        # Tambahkan bagian tubuh awal
        for i in range(1, self.length):
            self.positions.append((self.positions[0][0] - i, self.positions[0][1]))
    
    def get_head_position(self):
        return self.positions[0]
    
    def turn(self, point):
        # Mencegah ular berbalik ke arah berlawanan
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point
    
    def move(self):
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x) % GRID_WIDTH
        new_y = (head[1] + y) % GRID_HEIGHT
        new_position = (new_x, new_y)
        
        # Cek tabrakan dengan tubuh sendiri
        if new_position in self.positions[1:]:
            return False  # Game over
        
        self.positions.insert(0, new_position)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True
    
    def draw(self, surface):
        for i, p in enumerate(self.positions):
            # Buat kepala ular dengan warna berbeda
            if i == 0:
                color = GREEN
            else:
                # Gradasi warna untuk tubuh ular
                color = (0, 200 - (i * 2) % 100, 0)
            
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, DARK_GREEN, rect, 1)
    
    def grow(self):
        self.length += 1
        self.score += 10

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
    
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    
    def draw(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, (150, 0, 0), rect, 1)

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
        
    def draw_grid(self):
        for x in range(0, WIDTH, GRID_SIZE):
            for y in range(0, HEIGHT, GRID_SIZE):
                rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(self.screen, GRAY, rect, 1)
    
    def draw_score(self):
        score_text = self.font.render(f'Skor: {self.snake.score}', True, WHITE)
        high_score_text = self.font.render(f'Skor Tertinggi: {self.high_score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_score_text, (WIDTH - high_score_text.get_width() - 10, 10))
    
    def draw_game_over(self):
        game_over_text = self.big_font.render('GAME OVER', True, RED)
        restart_text = self.font.render('Tekan SPACE untuk melanjutkan', True, WHITE)
        self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))
    
    def check_win(self):
        # Jika ular memenuhi seluruh halaman, game selesai
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
                        # Reset game
                        self.snake.reset()
                        self.food.randomize_position()
                        self.game_over = False
                    elif event.key == pygame.K_UP:
                        self.snake.turn(UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.turn(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.turn(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.turn(RIGHT)
            
            if not self.game_over:
                # Gerakkan ular
                if not self.snake.move():
                    self.game_over = True
                    if self.snake.score > self.high_score:
                        self.high_score = self.snake.score
                
                # Cek jika ular memakan makanan
                if self.snake.get_head_position() == self.food.position:
                    self.snake.grow()
                    self.food.randomize_position()
                    # Pastikan makanan tidak muncul di tubuh ular
                    while self.food.position in self.snake.positions:
                        self.food.randomize_position()
                
                # Cek jika ular memenuhi seluruh halaman
                if self.check_win():
                    self.game_over = True
                    if self.snake.score > self.high_score:
                        self.high_score = self.snake.score
            
            # Gambar background
            self.screen.fill(BLACK)
            self.draw_grid()
            
            # Gambar ular dan makanan
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            
            # Gambar skor
            self.draw_score()
            
            # Gambar game over atau win screen
            if self.game_over:
                if self.check_win():
                    self.draw_win()
                else:
                    self.draw_game_over()
            
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()