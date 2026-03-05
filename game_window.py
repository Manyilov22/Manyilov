"""
Игровое окно на pygame
"""

import pygame
import random
import sys

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
        for car in player_data['cars']:
            if car['id'] == player_data['current_car']:
                self.current_car = car
                break
        
        if not self.current_car:
            self.current_car = player_data['cars'][0]
        
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
