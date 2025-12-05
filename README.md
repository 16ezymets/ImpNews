<div align="center">

# 📰 Important News Telegram Bot

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)
![python-telegram-bot](https://img.shields.io/badge/python--telegram--bot-≥20.7-blue?logo=telegram&logoColor=white)
![Telethon](https://img.shields.io/badge/telethon-≥1.28.5-0088cc?logo=telegram)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-≥2.0.23-red?logo=sqlalchemy)
![dotenv](https://img.shields.io/badge/python--dotenv-1.0.0+-green)

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Version](https://img.shields.io/badge/version-1.0.0-orange)

**Умный Telegram-бот для получения популярных новостей**  
*Актуальные новости • Персонализация • Уведомления*


</div>

---

## ✨ Возможности

### 📰 **Получение новостей**
- #### Свежие популярные новости в реальном времени
- #### Возможность добавлять каналы для мониторинга

### 🔔 **Уведомления**
- #### Push-уведомления о важных новостях
- #### Возможность ставить порог реакций для уведомлений
- #### Возможность включать и выключать мониторинг

---

## 🚀 Установка

### Предварительные требования
- #### Python 3.12 или выше
- #### Свой API_ID и API_HASH
- #### Telegram Bot Token от [@BotFather](https://t.me/BotFather)
- #### Доступ к интернету

### Шаг 1: Клонирование репозитория
```bash
git clone https://github.com/16ezymets/ImpNews
cd ImpNews
```
### Шаг 2: Настройка окружения
```bash
cp .env.example .env # Linux/Mac
# copy .env.eample .env - Windows

# ЗАПОЛНИТЕ СВОИ ДАННЫЕ В .env!
```
### Шаг 3: Установка зависимостей
```bash
python3 -m venv venv
source .venv/bin/activate # Linux/Mac
# venv/Scripts/activate - Windows
pip install -r requirements.txt
```
### Шаг 4: Авторизация бота как пользователя
```bash
python3 login.py
```
### Шаг 5: Запуск бота
```bash
python3 bot.py
```
## ⚙️ Конфигурация
### Файл .env
```env
API_ID=your_api_id
API_HASH=your_api_hash

BOT_TOKEN=your_bot_token_here

DATABASE_URL=sqlite:///news_bot.db
```

## 📖 Использование
### Команды
- #### `/start` - запустить бота
- #### `/add_channel @username` - добавить канал
- #### `/my_channels` - показать мои каналы
- #### `/remove_channel @username` - удалить канал
- #### `/set_min_reactions 100` - установить количество реакций
- #### `/start_monitoring`- начать мониторинг
- #### `/stop_monitoring` - остановить мониторинг

## 🏗️ Архитектура
```text
ImpNews/                           
├── bot.py                 # Телеграм-бот
├── login.py               # Авторизация бота как пользователя
├── db_utils.py            # Декоратор для работы с базой данных
├── sql_database.py        # База данных SQL
├── config.py              # Конфигурации бота
├── requirements.txt       # Необходимые библиотеки для запуска
├── .env                   # Окружение
└── README.md              # Документация
```

---

## Проверка кода
```
bash
```

---

## Отчет об ошибках
#### 1. Проверьте существующие [Issues](https://github.com/16ezymets/ImpNews/issues)
#### 2. Создайте новый issue с подробным описанием

## Предложение улучшений
#### 1. Обсудите идею в issues
#### 2. Создайте [Pull Request](https://github.com/16ezymets/ImpNews/pulls)

## Процесс Pull Request
#### 1. Форкните репозиторий
#### 2. Создайте ветку (```git checkout -b feature/AmazingFeature```)
#### 3. Закоммитьте изменения (```git commit -m 'Add AmazingFeature'```)
#### 4. Запушьте ветку (```git push origin feature/AmazingFeature```)
#### 5. Откройте [Pull Request](https://github.com/16ezymets/ImpNews/pulls)

---

## 👨‍💻 Автор
- #### GitHub: @16ezymets
- #### Telegram: @qprizz
- #### Проект: ImpNews

---

<div align='center'>
  
## ⭐ Если вам нравится проект, поставьте [звезду](https://api.star-history.com/svg?repos=16ezymets/ImpNews&type=Date) на GitHub!

</div>

