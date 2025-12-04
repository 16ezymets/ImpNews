# 📰 ImpNews Telegram Bot

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![aiogram](https://img.shields.io/badge/aiogram-3.x-green?logo=telegram)
![License](https://img.shields.io/badge/license-MIT-yellow)
![Status](https://img.shields.io/badge/status-active-brightgreen)
![Version](https://img.shields.io/badge/version-1.0.0-orange)

**Умный Telegram-бот для получения популярных новостей**  
*Актуальные новости • Персонализация • Уведомления*


</div>

---

## ✨ Возможности

### 📰 **Получение новостей**
- Свежие новости в реальном времени
- Агрегация из нескольких источников

### 🔔 **Уведомления**
- Push-уведомления о важных новостях
- Гибкая система подписок

---


## 🚀 Установка

### Предварительные требования
- Python 3.10 или выше
- Свой API_ID и API_HASH
- Telegram Bot Token от [@BotFather](https://t.me/BotFather)
- Доступ к интернету

### Шаг 1: Клонирование репозитория
```bash
git clone https://github.com/16ezymets/ImpNews.git
cd ImpNews
```
### Шаг 2: Настройка окружения
```bash
cp .env.example .env
# ЗАПОЛНИТЕ СВОИ ДАННЫЕ В .env!
```
### Шаг 3: Установка зависимостей
```bash
python -m venv venv
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
### Основные команды
```text
/start - запустить бота
/add_channel @username - добавить
/my_channels - показать мои каналы
/remove_channel @username - удалить канал
/set_min_reactions 100 - установить количество реакций
/start_monitoring - начать мониторинг
/stop_monitoring - остановить мониторинг
```

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
#### 1. Проверьте существующие [issues](https://github.com/16ezymets/ImpNews/issues)
#### 2. Создайте новый issue с подробным описанием

## Предложение улучшений
#### 1. Обсудите идею в issues
#### 2. Создайте Pull Request

## Процесс Pull Request
#### 1. Форкните репозиторий
#### 2. Создайте ветку (```git checkout -b feature/AmazingFeature```)
#### 3. Закоммитьте изменения (```git commit -m 'Add AmazingFeature'```)
#### 4. Запушьте ветку (```git push origin feature/AmazingFeature```)
#### 5. Откройте Pull Request

---

## 📄 Лицензия
Этот проект распространяется под лицензией MIT. См. файл LICENSE для подробностей.

---

## 👨‍💻 Автор
- #### GitHub: @16ezymets
- #### Telegram: @qprizz
- #### Проект: ImpNews

---

## 📊 Статистика проекта

<div align="center">

![GitHub Stars](https://img.shields.io/github/stars/16ezymets/ImpNews?style=for-the-badge&logo=github&color=yellow)
![GitHub Forks](https://img.shields.io/github/forks/16ezymets/ImpNews?style=for-the-badge&logo=github&color=blue)
![GitHub Issues](https://img.shields.io/github/issues/16ezymets/ImpNews?style=for-the-badge&logo=github&color=red)
![GitHub Pull Requests](https://img.shields.io/github/issues-pr/16ezymets/ImpNews?style=for-the-badge&logo=github&color=green)
![GitHub License](https://img.shields.io/github/license/16ezymets/ImpNews?style=for-the-badge&logo=opensourceinitiative&color=orange)

</div>

### 📈 Детальная статистика
| Метрика | Значение | Тенденция |
|---------|----------|-----------|
| **⭐ Звезды** | ![Stars](https://img.shields.io/github/stars/16ezymets/ImpNews?label=&style=flat-square) | ![Star Growth](https://img.shields.io/github/stars/16ezymets/ImpNews?style=social) |
| **🍴 Форки** | ![Forks](https://img.shields.io/github/forks/16ezymets/ImpNews?label=&style=flat-square) | ![Fork Growth](https://img.shields.io/github/forks/16ezymets/ImpNews?style=social) |
| **🐛 Issues** | ![Issues](https://img.shields.io/github/issues/16ezymets/ImpNews?label=&style=flat-square) | ![Issues Closed](https://img.shields.io/github/issues-closed/16ezymets/ImpNews?label=closed&style=flat-square) |
| **🔄 PR** | ![PRs](https://img.shields.io/github/issues-pr/16ezymets/ImpNews?label=&style=flat-square) | ![PRs Closed](https://img.shields.io/github/issues-pr-closed/16ezymets/ImpNews?label=merged&style=flat-square) |
| **📏 Размер** | ![Repo Size](https://img.shields.io/github/repo-size/16ezymets/ImpNews?label=&style=flat-square) | ![Languages](https://img.shields.io/github/languages/code-size/16ezymets/ImpNews?style=flat-square) |
| **📅 Последний коммит** | ![Last Commit](https://img.shields.io/github/last-commit/16ezymets/ImpNews?label=&style=flat-square) | ![Commit Activity](https://img.shields.io/github/commit-activity/m/16ezymets/ImpNews?label=активность&style=flat-square) |

### 🌟 История звезд
[![Star History Chart](https://api.star-history.com/svg?repos=16ezymets/ImpNews&type=Timeline)](https://star-history.com/#16ezymets/ImpNews&Timeline)

### 📊 Используемые языки
```text
Python:   ██████████████████████████ 95.2%
Makefile: ████ 4.5%
Other:    ░ 0.3%

