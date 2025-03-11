#!/usr/bin/env python3
import cv2
import numpy as np
from PIL import Image
import time
import os
from ppadb.client import Client as AdbClient

class DodoPizzaBot:
    def __init__(self):
        # Инициализация ADB
        self.client = AdbClient(host="127.0.0.1", port=5037)
        self.device = None
        self.connect_device()
        
        # Константы для определения цветов и областей
        self.TOWER_COLOR_LOWER = np.array([0, 0, 100])  # Красноватый цвет башни
        self.TOWER_COLOR_UPPER = np.array([80, 80, 255])
        self.PLATFORM_COLOR_LOWER = np.array([20, 20, 20])  # Серый цвет платформы
        self.PLATFORM_COLOR_UPPER = np.array([100, 100, 100])
        
        # Область поиска (можно настроить под конкретное устройство)
        self.SEARCH_AREA_Y = [800, 1600]  # Примерная область где находится игра
        self.TAP_COORDS = (540, 2000)  # Координаты для нажатия

    def connect_device(self):
        """Подключение к устройству через ADB"""
        devices = self.client.devices()
        if len(devices) == 0:
            raise Exception("Устройство не найдено")
        self.device = devices[0]
        print("Устройство подключено успешно")

    def take_screenshot(self):
        """Получение скриншота с устройства"""
        screenshot = self.device.screencap()
        image = Image.frombytes('RGB', (1080, 2400), screenshot)
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    def find_game_elements(self, image):
        """Поиск элементов игры на экране"""
        # Обрезаем изображение до области поиска
        game_area = image[self.SEARCH_AREA_Y[0]:self.SEARCH_AREA_Y[1], :]
        
        # Создаем маски для башни и платформы
        tower_mask = cv2.inRange(game_area, self.TOWER_COLOR_LOWER, self.TOWER_COLOR_UPPER)
        platform_mask = cv2.inRange(game_area, self.PLATFORM_COLOR_LOWER, self.PLATFORM_COLOR_UPPER)
        
        # Находим контуры
        tower_contours, _ = cv2.findContours(tower_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        platform_contours, _ = cv2.findContours(platform_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Находим самые большие контуры (это будут наши объекты)
        tower = max(tower_contours, key=cv2.contourArea) if tower_contours else None
        platform = max(platform_contours, key=cv2.contourArea) if platform_contours else None
        
        if tower is not None and platform is not None:
            # Получаем центры объектов
            tower_M = cv2.moments(tower)
            tower_cx = int(tower_M['m10'] / tower_M['m00'])
            
            platform_M = cv2.moments(platform)
            platform_cx = int(platform_M['m10'] / platform_M['m00'])
            
            return tower_cx, platform_cx
        return None, None

    def should_tap(self, tower_x, platform_x):
        """Определяет нужно ли нажимать"""
        # Допустимая погрешность в пикселях
        TOLERANCE = 10
        return abs(tower_x - platform_x) <= TOLERANCE

    def tap(self, x, y):
        """Нажатие на экран в указанных координатах"""
        self.device.shell(f'input tap {x} {y}')

    def run(self):
        """Основной цикл работы бота"""
        print("Запуск бота...")
        last_tap_time = 0
        TAP_COOLDOWN = 1.0  # Задержка между нажатиями в секундах
        
        while True:
            try:
                screen = self.take_screenshot()
                tower_x, platform_x = self.find_game_elements(screen)
                
                current_time = time.time()
                if tower_x is not None and platform_x is not None:
                    if self.should_tap(tower_x, platform_x) and current_time - last_tap_time > TAP_COOLDOWN:
                        self.tap(*self.TAP_COORDS)
                        last_tap_time = current_time
                        print("Тап! Башня поставлена")
                
                time.sleep(0.1)  # Небольшая задержка для снижения нагрузки
                
            except KeyboardInterrupt:
                print("Бот остановлен")
                break
            except Exception as e:
                print(f"Ошибка: {e}")
                continue

if __name__ == "__main__":
    bot = DodoPizzaBot()
    bot.run() 