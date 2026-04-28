import tkinter as tk
import pygame
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from menu_window import MenuWindow

def main():
    """Запуск игры"""
    print("Запуск Traffic Racer...")
    
    # Инициализация pygame
    pygame.init()
    
    # Создание и запуск главного меню
    root = tk.Tk()
    app = MenuWindow(root)
    root.mainloop()
    
    # Завершение работы
    pygame.quit()
    print("Игра закрыта")

if __name__ == "__main__":
    main()
