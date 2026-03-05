"""
Главное меню игры 
"""

import tkinter as tk
from tkinter import messagebox
import pygame
from garage_window import GarageWindow
from game_window import GameWindow
from data.save_data import SaveData

class MenuWindow:
    """Класс главного меню"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Traffic Racer - Меню")
        self.root.geometry("500x600")
        self.root.configure(bg="#2c3e50")
        
        # Загрузка данных
        self.save_data = SaveData()
        self.player_data = self.save_data.load()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Обработка закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """Создание элементов интерфейса"""
        
        # Заголовок
        title = tk.Label(
            self.root,
            text="TRAFFIC RACER",
            font=("Arial", 24, "bold"),
            fg="#3498db",
            bg="#2c3e50"
        )
        title.pack(pady=30)
        
        # Информация об игроке
        info_frame = tk.Frame(self.root, bg="#34495e", relief="solid", bd=2)
        info_frame.pack(pady=20, padx=50, fill="x")
        
        # Монеты
        coins_label = tk.Label(
            info_frame,
            text=f" Монеты: {self.player_data['coins']}",
            font=("Arial", 14),
            fg="#f1c40f",
            bg="#34495e"
        )
        coins_label.pack(pady=5)
        
        # Рекорд
        record_label = tk.Label(
            info_frame,
            text=f" Рекорд: {self.player_data['high_score']} м",
            font=("Arial", 14),
            fg="#e74c3c",
            bg="#34495e"
        )
        record_label.pack(pady=5)
        
        # Текущая машина
        current_car = self.get_current_car_name()
        car_label = tk.Label(
            info_frame,
            text=f" Машина: {current_car}",
            font=("Arial", 14),
            fg="#2ecc71",
            bg="#34495e"
        )
        car_label.pack(pady=5)
        
        # Кнопки
        button_frame = tk.Frame(self.root, bg="#2c3e50")
        button_frame.pack(pady=30)
        
        # Кнопка "Играть"
        play_btn = tk.Button(
            button_frame,
            text="▶ НАЧАТЬ ИГРУ",
            font=("Arial", 14, "bold"),
            bg="#27ae60",
            fg="white",
            width=20,
            height=2,
            command=self.start_game
        )
        play_btn.pack(pady=10)
        
        # Кнопка "Гараж"
        garage_btn = tk.Button(
            button_frame,
            text="ГАРАЖ",
            font=("Arial", 14, "bold"),
            bg="#3498db",
            fg="white",
            width=20,
            height=2,
            command=self.open_garage
        )
        garage_btn.pack(pady=10)
        
        # Кнопка "Выход"
        exit_btn = tk.Button(
            button_frame,
            text="✕ ВЫХОД",
            font=("Arial", 14, "bold"),
            bg="#e74c3c",
            fg="white",
            width=20,
            height=2,
            command=self.on_closing
        )
        exit_btn.pack(pady=10)
    
    def get_current_car_name(self):
        """Получение названия текущей машины"""
        for car in self.player_data['cars']:
            if car['id'] == self.player_data['current_car']:
                return car['name']
        return "Неизвестно"
    
    def start_game(self):
        """Запуск игры"""
        self.root.withdraw()  # Скрываем меню
        
        # Создаем окно игры
        game = GameWindow(self.player_data, self.return_to_menu)
        game.run()
    
    def open_garage(self):
        """Открытие гаража"""
        self.root.withdraw()  # Скрываем меню
        
        # Создаем окно гаража
        garage_root = tk.Toplevel()
        garage = GarageWindow(garage_root, self.player_data, self.return_to_menu)
    
    def return_to_menu(self, updated_data=None):
        """Возврат в меню"""
        if updated_data:
            self.player_data = updated_data
            self.save_data.save(updated_data)
        
        # Обновляем интерфейс
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_widgets()
        
        # Показываем меню
        self.root.deiconify()
    
    def on_closing(self):
        """При закрытии окна"""
        if messagebox.askokcancel("Выход", "Вы хотите выйти из игры?"):
            self.save_data.save(self.player_data)
            self.root.quit()
