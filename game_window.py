import pygame
import random
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from data.save_data import CARS

# Константы
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
ROAD_WIDTH = 300
LANE_WIDTH = ROAD_WIDTH // 3

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)
ROAD_COLOR = (50, 50, 50)

class GameWindow:
    """Класс игры"""
    
    def __init__(self, player_data, return_callback):
        self.player_data = player_data
        self.return_callback = return_callback
        
        # Настройки экрана
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Traffic Racer - Игра")
        
        # Шрифты
        self.font_big = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 24)
        
        # Получаем текущую машину
        self.current_car = None
        for car in CARS:
            if car['id'] == player_data['current_car']:
                self.current_car = car
                break
        
        if not self.current_car:
            self.current_car = CARS[0]
        
        # Игрок
        self.player_x = SCREEN_WIDTH // 2 - 20
        self.player_y = SCREEN_HEIGHT - 150
        self.player_speed = self.current_car['speed']
        self.player_rect = pygame.Rect(self.player_x, self.player_y, 40, 70)
        
        # Игровые объекты
        self.enemies = []
        self.coins = []
        self.score = 0
        self.distance = 0
        self.coins_collected = 0
        self.lives = 3
        
        # Таймеры
        self.spawn_timer = 0
        self.coin_timer = 0
        self.clock = pygame.time.Clock()
        
        # Состояние игры
        self.running = True
        self.game_over = False
        
        # Управление
        self.move_left = False
        self.move_right = False
    
    def run(self):
        """Основной цикл игры"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # 60 FPS
        
        # Возврат в меню
        self.return_callback(self.player_data)
    
    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move_left = True
                elif event.key == pygame.K_RIGHT:
                    self.move_right = True
                elif event.key == pygame.K_r and self.game_over:
                    self.restart()
                elif event.key == pygame.K_m and self.game_over:
                    self.running = False
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.move_left = False
                elif event.key == pygame.K_RIGHT:
                    self.move_right = False
    
    def update(self):
        """Обновление игры"""
        if self.game_over:
            return

        # Движение игрока(в разработке)
        if self.move_left and self.player_x > SCREEN_WIDTH // 2 - ROAD_WIDTH // 2:
            self.player_x -= self.player_speed
        if self.move_right and self.player_x < SCREEN_WIDTH // 2 + ROAD_WIDTH // 2 - 40:
            self.player_x += self.player_speed
        
        self.player_rect.x = self.player_x
        
        # Пройденное расстояние
        self.distance += self.player_speed / 10
        self.score = int(self.distance * 10 + self.coins_collected * 5)
        
        # Спавн врагов
        self.spawn_timer += 1
        if self.spawn_timer > 40:
            self.spawn_timer = 0
            if random.random() < 0.5:
                self.spawn_enemy()

        # Спавн монет
        self.spawn_timer += 1
        if self.spawn_timer > 40:
            self.spawn_timer = 0
            if random.random() < 0.5:
                self.spawn_enemy()
                
        self.coin_timer += 1
        if self.coin_timer > 30:
            self.coin_timer = 0
            if random.random() < 0.3:
                self.spawn_coin()
        
        # Обновление врагов
        for enemy in self.enemies[:]:
            enemy.y += 5
            enemy_rect = pygame.Rect(enemy.x, enemy.y, 40, 70)
            
            if enemy.y > SCREEN_HEIGHT:
                self.enemies.remove(enemy)
            elif self.player_rect.colliderect(enemy_rect):
                self.enemies.remove(enemy)
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
                    self.update_high_score()
        
        # Обновление монет
        for coin in self.coins[:]:
            coin.y += 5
            coin_rect = pygame.Rect(coin.x, coin.y, 25, 25)
            
            if coin.y > SCREEN_HEIGHT:
                self.coins.remove(coin)
            elif self.player_rect.colliderect(coin_rect):
                self.coins.remove(coin)
                self.coins_collected += 10
                self.player_data['coins'] += 10
                
    def spawn_enemy(self):
        lane = random.randint(0, 2)
        x = SCREEN_WIDTH // 2 - ROAD_WIDTH // 2 + lane * LANE_WIDTH + 5
        
        enemy = type('Enemy', (), {})()
        enemy.x = x
        enemy.y = -100
        enemy.color = random.choice([RED, GREEN, BLUE, YELLOW])
        
        self.enemies.append(enemy)
    
    def spawn_coin(self):
        lane = random.randint(0, 2)
        x = SCREEN_WIDTH // 2 - ROAD_WIDTH // 2 + lane * LANE_WIDTH + 20
        
        coin = type('Coin', (), {})()
        coin.x = x
        coin.y = -50
        
        self.coins.append(coin)
        
    def update_high_score(self):
        if self.score > self.player_data['high_score']:
            self.player_data['high_score'] = self.score
    
    def restart(self):
        self.enemies = []
        self.coins = []
        self.score = 0
        self.distance = 0
        self.coins_collected = 0
        self.lives = 3
        self.player_x = SCREEN_WIDTH // 2 - 20
        self.player_rect.x = self.player_x
        self.game_over = False
        
    def draw(self):
        self.screen.fill(ROAD_COLOR)
        
        road_left = SCREEN_WIDTH // 2 - ROAD_WIDTH // 2
        road_right = SCREEN_WIDTH // 2 + ROAD_WIDTH // 2
        
        pygame.draw.rect(self.screen, GRAY, (road_left, 0, ROAD_WIDTH, SCREEN_HEIGHT))
        
        for i in range(0, SCREEN_HEIGHT, 50):
            center_x = SCREEN_WIDTH // 2
            pygame.draw.line(self.screen, WHITE, (center_x, i), (center_x, i + 30), 3)
        
        pygame.draw.line(self.screen, WHITE, (road_left, 0), (road_left, SCREEN_HEIGHT), 2)
        pygame.draw.line(self.screen, WHITE, (road_right, 0), (road_right, SCREEN_HEIGHT), 2)
        
        for enemy in self.enemies:
            pygame.draw.rect(self.screen, enemy.color, (enemy.x, enemy.y, 40, 70))
        
        for coin in self.coins:
            pygame.draw.circle(self.screen, YELLOW, (coin.x + 12, coin.y + 12), 12)
        
        pygame.draw.rect(self.screen, self.current_car['color'], self.player_rect)
        pygame.draw.rect(self.screen, YELLOW, (self.player_x + 5, self.player_y - 5, 5, 5))
        pygame.draw.rect(self.screen, YELLOW, (self.player_x + 30, self.player_y - 5, 5, 5))
        pygame.draw.rect(self.screen, (200, 200, 255), (self.player_x + 5, self.player_y + 10, 10, 15))
        pygame.draw.rect(self.screen, (200, 200, 255), (self.player_x + 25, self.player_y + 10, 10, 15))
        
        score_text = self.font_small.render(f"Счет: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        coins_text = self.font_small.render(f"Монеты: {self.coins_collected}", True, YELLOW)
        self.screen.blit(coins_text, (10, 35))
        
        lives_text = self.font_small.render(f"Жизни: {self.lives}", True, RED)
        self.screen.blit(lives_text, (10, 60))
        
        distance_text = self.font_small.render(f"Дистанция: {int(self.distance)} м", True, WHITE)
        self.screen.blit(distance_text, (10, 85))
        
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font_big.render("GAME OVER", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(game_over_text, text_rect)
            
            score_text = self.font_small.render(f"Счет: {self.score}", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(score_text, score_rect)
            
            if self.score == self.player_data['high_score'] and self.score > 0:
                record_text = self.font_small.render("НОВЫЙ РЕКОРД!", True, YELLOW)
                record_rect = record_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 25))
                self.screen.blit(record_text, record_rect)
            
            restart_text = self.font_small.render("Нажми R для рестарта, M для меню", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
