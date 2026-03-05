python

"""
Окно гаража для выбора и покупки машин
"""

import tkinter as tk
from tkinter import messagebox
from data.car_data import CARS
from data.save_data import SaveData

class GarageWindow:
    """Класс гаража"""
    
    def __init__(self, root, player_data, return_callback):
        self.root = root
        self.root.title("Traffic Racer - Гараж")
        self.root.geometry("600x700")
        self.root.configure(bg="#34495e")
        
        self.player_data = player_data
        self.return_callback = return_callback
        
        # Создание интерфейса
        self.create_widgets()
        
        # Обработка закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """Создание интерфейса"""
        
        # Заголовок
        title = tk.Label(
            self.root,
            text="ГАРАЖ",
            font=("Arial", 24, "bold"),
            fg="#3498db",
            bg="#34495e"
        )
        title.pack(pady=20)
        
        # Монеты
        coins_label = tk.Label(
            self.root,
            text=f"Монеты: {self.player_data['coins']}",
            font=("Arial", 18, "bold"),
            fg="#f1c40f",
            bg="#34495e"
        )
        coins_label.pack(pady=10)
        
        # Контейнер для машин с прокруткой
        canvas = tk.Canvas(self.root, bg="#2c3e50", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        self.cars_frame = tk.Frame(canvas, bg="#2c3e50")
        
        self.cars_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.cars_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Добавляем все машины
        for car in CARS:
            self.add_car_to_list(car)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")
        
        # Кнопка "Назад"
        back_btn = tk.Button(
            self.root,
            text="← НАЗАД",
            font=("Arial", 14, "bold"),
            bg="#95a5a6",
            fg="white",
            width=15,
            height=1,
            command=self.on_closing
        )
        back_btn.pack(pady=20)
    
    def add_car_to_list(self, car):
        """Добавление машины в список"""
        
        # Определяем, есть ли машина у игрока
        is_owned = car['id'] in [c['id'] for c in self.player_data['cars']]
        is_current = car['id'] == self.player_data['current_car']
        
        # Фрейм для машины
        car_frame = tk.Frame(
            self.cars_frame,
            bg="#34495e" if is_current else "#2c3e50",
            relief="solid",
            bd=2
        )
        car_frame.pack(fill="x", pady=5, padx=5)
        
        # Цветной квадратик
        color_str = f'#{car["color"][0]:02x}{car["color"][1]:02x}{car["color"][2]:02x}'
        color_box = tk.Frame(car_frame, bg=color_str, width=60, height=60)
        color_box.pack(side="left", padx=10, pady=10)
        color_box.pack_propagate(False)
        
        # Информация
        info_frame = tk.Frame(car_frame, bg=car_frame['bg'])
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Название
        name_label = tk.Label(
            info_frame,
            text=car['name'],
            font=("Arial", 14, "bold"),
            fg="white",
            bg=car_frame['bg'],
            anchor="w"
        )
        name_label.pack(anchor="w")
        
        # Характеристики
        stats_label = tk.Label(
            info_frame,
            text=f"Скорость: {car['speed']}/10 | Управление: {car['handling']}/10",
            font=("Arial", 10),
            fg="#bdc3c7",
            bg=car_frame['bg'],
            anchor="w"
        )
        stats_label.pack(anchor="w")
        
        # Действия
        if is_owned:
            if is_current:
                status_label = tk.Label(
                    info_frame,
                    text="✓ ВЫБРАНА",
                    font=("Arial", 10, "bold"),
                    fg="#2ecc71",
                    bg=car_frame['bg']
                )
                status_label.pack(anchor="w")
            else:
                select_btn = tk.Button(
                    info_frame,
                    text="Выбрать",
                    font=("Arial", 10, "bold"),
                    bg="#3498db",
                    fg="white",
                    command=lambda c=car: self.select_car(c)
                )
                select_btn.pack(anchor="w", pady=2)
        else:
            price_label = tk.Label(
                info_frame,
                text=f"{car['price']} монет",
                font=("Arial", 10, "bold"),
                fg="#f1c40f",
                bg=car_frame['bg']
            )
            price_label.pack(anchor="w")
            
            if self.player_data['coins'] >= car['price']:
                buy_btn = tk.Button(
                    info_frame,
                    text="Купить",
                    font=("Arial", 10, "bold"),
                    bg="#27ae60",
                    fg="white",
                    command=lambda c=car: self.buy_car(c)
                )
                buy_btn.pack(anchor="w", pady=2)
            else:
                need_label = tk.Label(
                    info_frame,
                    text=f"Не хватает {car['price'] - self.player_data['coins']} монет",
                    font=("Arial", 10),
                    fg="#e74c3c",
                    bg=car_frame['bg']
                )
                need_label.pack(anchor="w", pady=2)
    
    def select_car(self, car):
        """Выбор машины"""
        self.player_data['current_car'] = car['id']
        messagebox.showinfo("Успешно", f"Выбрана машина: {car['name']}")
        
        # Обновляем интерфейс
        for widget in self.cars_frame.winfo_children():
            widget.destroy()
        
        for c in CARS:
            self.add_car_to_list(c)
    
    def buy_car(self, car):
        """Покупка машины"""
        if messagebox.askyesno("Покупка", f"Купить {car['name']} за {car['price']} монет?"):
            self.player_data['coins'] -= car['price']
            self.player_data['cars'].append(car)
            self.player_data['current_car'] = car['id']
            
            messagebox.showinfo("Поздравляем!", f"Теперь у вас есть {car['name']}!")
            
            # Обновляем интерфейс
            for widget in self.cars_frame.winfo_children():
                widget.destroy()
            
            for c in CARS:
                self.add_car_to_list(c)
    
    def on_closing(self):
        """Закрытие окна"""
        self.return_callback(self.player_data)
        self.root.destroy()
