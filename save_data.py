"""
Класс для сохранения и загрузки данных
"""

import json
import os

CARS = [
    {
        'id': 0,
        'name': 'Стартовая машина',
        'price': 0,
        'speed': 5,
        'handling': 5,
        'color': (0, 100, 255)
    },
    {
        'id': 1,
        'name': 'Спортивная машина',
        'price': 200,
        'speed': 8,
        'handling': 7,
        'color': (255, 0, 0)
    },
    {
        'id': 2,
        'name': 'Внедорожник',
        'price': 150,
        'speed': 4,
        'handling': 8,
        'color': (0, 255, 0)
    },
    {
        'id': 3,
        'name': 'Гоночный болид',
        'price': 500,
        'speed': 10,
        'handling': 9,
        'color': (255, 255, 0)
    },
    {
        'id': 4,
        'name': 'Кабриолет',
        'price': 300,
        'speed': 7,
        'handling': 6,
        'color': (255, 150, 200)
    },
    {
        'id': 5,
        'name': 'Мини-кар',
        'price': 100,
        'speed': 6,
        'handling': 5,
        'color': (150, 150, 150)
    }
]

SAVE_FILE = "save.json"

class SaveData:
    """Класс для работы с сохранениями"""
    
    def load(self):
        """Загрузка данных из файла"""
        default_data = {
            'coins': 200,
            'high_score': 0,
            'current_car': 0,
            'cars': [CARS[0].copy()]
        }
        
        try:
            if os.path.exists(SAVE_FILE):
                with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for key in default_data:
                        if key not in data:
                            data[key] = default_data[key]
                    return data
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
        
        return default_data
    
    def save(self, data):
        """Сохранение данных в файл"""
        try:
            with open(SAVE_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
            return False
