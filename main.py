import tkinter as tk
from menu_window import MenuWindow
import pygame

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
    screen.blit(text, (50, 100))
  
    pygame.display.flip()
pygame.quit()
