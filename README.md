# JjsAi21

**English** | [Русский](#русский)

---

## 🇬🇧 English

### Overview

JjsAi21 is version 2.1 of JjsAI - an artificial intelligence designed to play **Jujutsu Shenanigans**, a Roblox game based on the popular anime/manga series "Jujutsu Kaisen". This AI is trained using video footage to learn gameplay mechanics and strategies.

### Features

- 🎮 Automated gameplay for Jujutsu Shenanigans
- 🧠 Video-based learning system
- 🔄 Continuous improvement through observation
- ⚡ Optimized for real-time decision making

### How It Works

The AI learns by analyzing video recordings of gameplay sessions. It processes visual information to understand:
- Character movements and combat mechanics
- Ability usage and timing
- Strategic decision-making patterns
- Enemy behavior recognition

### Requirements

- Python 3.8 or higher
- Required dependencies (see `requirements.txt`)
- Video footage for training
- Roblox client installed

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd JjsAi21

# Install dependencies
pip install -r requirements.txt

# Run the AI
python main.py
```

### Usage / Использование

1. Prepare training videos of Jujutsu Shenanigans gameplay / Подготовьте обучающие видео с геймплеем Jujutsu Shenanigans
2. Place videos in the `videos/` folder / Поместите видео в папку `videos/`
3. Label your videos using the labeling tool / Разметьте видео с помощью инструмента разметки:
   ```bash
   python label_generator.py videos/your_video.mp4
   ```
4. Update dependencies (optional) / Обновить зависимости (опционально):
   ```bash
   # Windows
   setup_update.bat
   ```
5. Start the training process / Запустите процесс обучения:
   ```bash
   # Windows
   start_training.bat
   
   # Linux/Mac
   python train.py --mode train
   ```
6. Analyze videos with trained AI / Анализируйте видео с помощью обученного ИИ:
   ```bash
   # Windows
   start_ai.bat
   
   # Linux/Mac
   python train.py --mode analyze --video path/to/video.mp4
   ```

### Project Structure / Структура Проекта

```
JjsAi21/
├── README.md                 # Project documentation (EN/RU)
├── train.py                  # Main AI training and analysis module
├── label_generator.py        # Tool for labeling training videos
├── requirements.txt          # Python dependencies
├── setup_update.bat          # Windows script to update pip and install libraries
├── start_training.bat        # Windows launcher for training
├── start_ai.bat              # Windows launcher for AI analysis
├── r_skill_description.txt   # R-skill configuration (Player Swap)
│
├── videos/                   # Place training videos here
├── labels/                   # Label files (JSON) - created automatically
│
├── models/
│   └── best_model.pth        # Trained model weights
│
└── logs/
    ├── training.log          # Training process logs
    └── analysis_results_*.json # Video analysis results
```

### License

This project is provided as-is for educational purposes.

### Disclaimer

This AI is designed for educational and research purposes. Please respect the game's terms of service and community guidelines when using automated tools.

---

## 🇷🇺 Русский

### Обзор

JjsAi21 — это версия 2.1 проекта JjsAI, искусственный интеллект, созданный для игры в **Jujutsu Shenanigans** — игру в Roblox, основанную на популярном аниме/манге «Магическая битва». Этот ИИ обучается на видеозаписях игрового процесса.

### Возможности

- 🎮 Автоматизированный геймплей в Jujutsu Shenanigans
- 🧠 Система обучения на основе видео
- 🔄 Непрерывное улучшение через наблюдение
- ⚡ Оптимизировано для принятия решений в реальном времени

### Как это работает

ИИ обучается путем анализа видеозаписей игровых сессий. Он обрабатывает визуальную информацию для понимания:
- Перемещения персонажей и механик боя
- Использования способностей и тайминга
- Паттернов стратегического принятия решений
- Распознавания поведения противников

### Требования

- Python 3.8 или выше
- Необходимые зависимости (см. `requirements.txt`)
- Видеоматериалы для обучения
- Установленный клиент Roblox

### Установка

```bash
# Клонировать репозиторий
git clone <url-репозитория>
cd JjsAi21

# Установить зависимости
pip install -r requirements.txt

# Запустить ИИ
python main.py
```

### Использование

1. Подготовьте обучающие видео с геймплеем Jujutsu Shenanigans
2. Поместите видео в папку `videos/`
3. Разметьте видео с помощью инструмента разметки:
   ```bash
   python label_generator.py videos/your_video.mp4
   ```
4. Обновить зависимости (опционально):
   ```bash
   # Windows
   setup_update.bat
   ```
5. Запустите процесс обучения:
   ```bash
   # Windows
   start_training.bat
   
   # Linux/Mac
   python train.py --mode train
   ```
6. Анализируйте видео с помощью обученного ИИ:
   ```bash
   # Windows
   start_ai.bat
   
   # Linux/Mac
   python train.py --mode analyze --video path/to/video.mp4
   ```

### Структура проекта

```
JjsAi21/
├── README.md                 # Документация проекта (EN/RU)
├── train.py                  # Основной модуль обучения и анализа ИИ
├── label_generator.py        # Инструмент для разметки обучающих видео
├── requirements.txt          # Python зависимости
├── setup_update.bat          # Скрипт обновления pip и установки библиотек (Windows)
├── start_training.bat        # Запуск обучения (Windows)
├── start_ai.bat              # Запуск анализа ИИ (Windows)
├── r_skill_description.txt   # Описание R-скилла (Свап позиций)
│
├── videos/                   # Обучающие видео
├── labels/                   # Файлы разметки (JSON) - создаётся автоматически
│
├── models/
│   └── best_model.pth        # Веса обученной модели
│
└── logs/
    ├── training.log          # Логи процесса обучения
    └── analysis_results_*.json # Результаты анализа видео
```

### Лицензия

Этот проект предоставляется «как есть» в образовательных целях.

### Отказ от ответственности

Этот ИИ предназначен для образовательных и исследовательских целей. Пожалуйста, соблюдайте условия использования игры и правила сообщества при использовании инструментов автоматизации.

---

**Version / Версия:** 2.1  
**Author / Автор:** JjsAI Team
