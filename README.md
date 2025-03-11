# DodoPizza Tower Bot

Бот для автоматизации мини-игры DodoPizza Tower в Termux.

## Требования

- Установленный Termux
- Python 3.8+
- ADB (Android Debug Bridge)
- USB-отладка включена на устройстве

## Установка

1. Установите Termux из F-Droid
2. Установите необходимые пакеты в Termux:
```bash
pkg update && pkg upgrade
pkg install python opencv-python android-tools
```

3. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/dodopizza-tower-bot
cd dodopizza-tower-bot
```

4. Установите зависимости Python:
```bash
pip install -r requirements.txt
```

## Использование

1. Подключите устройство через USB и включите USB-отладку
2. Запустите ADB сервер:
```bash
adb start-server
```

3. Запустите бота:
```bash
python main.py
```

## Функционал

- Автоматическое определение элементов игры на экране
- Точное определение момента для нажатия
- Автоматическая игра

## Примечания

- Убедитесь, что USB-отладка включена в настройках разработчика
- Для работы необходимо разрешение на использование ADB
- Рекомендуется использовать устройство с разрешением экрана 1080x2400 