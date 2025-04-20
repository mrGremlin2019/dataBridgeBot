# 🤖 Telegram Bot на Python

Telegram‑бот на Python (Aiogram + Aiohttp), который:
- Получает данные из открытого API (JSONPlaceholder)
- Преобразует поля из `camelCase` в `snake_case` и валидирует через Pydantic
- Сохраняет пользователей в PostgreSQL и Google Sheets
- Разворачивается через Docker Compose и проксируется Nginx

---

## 🚀 Функциональность

### 📌 `/start`
- Отправляет приветственное сообщение и инлайн‑кнопки

### 📌 Получить данные
- Запрос к JSONPlaceholder (`https://jsonplaceholder.typicode.com/users`)
- Преобразование ключей в `snake_case`
- Валидация Pydantic
- Отправка списка пользователей в чат

### 📌 Сохранить данные
- Сохраняет валидированные данные в PostgreSQL
- Добавляет записи в Google Sheets
- Уведомляет об успехе или ошибке

---

## ⚙️ Технологии

- **Python 3.10**  
- **Aiogram** — Telegram Bot API  
- **Aiohttp** — HTTP‑сервер для вебхуков  
- **Dependency Injector** — внедрение зависимостей  
- **Pydantic** — валидация и преобразование данных  
- **SQLAlchemy + asyncpg** — асинхронная работа с PostgreSQL  
- **gspread** — Google Sheets API  
- **Nginx** — проксирование HTTPS → webhook  
- **Docker & Docker Compose** — контейнеризация  
- **Let’s Encrypt** — SSL сертификаты  

---

## 📂 Структура проекта

```bash
telegram-bot-project/
├── docker-compose.yml       # Описание сервисов (Postgres, Bot, Nginx)
├── Dockerfile               # Сборка контейнера бота
├── nginx.conf               # Конфиг Nginx для проксирования webhook
├── .env                     # Переменные окружения
├── creds.json               # Учетные данные Google Sheets
├── requirements.txt         # Python-зависимости
└── src/
    ├── main.py              # Точка входа (web.run_app)
    ├── server.py            # Настройка aiohttp-приложения
    ├── bot/
    │   ├── bot.py           # Dispatcher + Bot через DI
    │   ├── config_bot.py    # Pydantic‑настройки бота
    │   ├── handlers.py      # Хендлеры команд и callback
    │   ├── keyboards.py     # Инлайн‑кнопки
    │   └── webhook.py       # Установка webhook
    ├── DI/
    │   └── container.py     # Dependency Injector
    ├── api/
    │   └── user_service.py  # Клиент JSONPlaceholder
    ├── db/
    │   ├── config_db.py     # Pydantic‑настройки и SQLAlchemy
    │   ├── crud.py          # Репозиторий пользователей
    │   └── models.py        # SQLAlchemy‑модель User
    ├── schemas/
    │   └── user.py          # Pydantic‑схемы
    └── utils/
        ├── converters.py    # camelCase → snake_case
        └── google_sheets.py # Интеграция с Google Sheets
```

---

## 🐳 Запуск через Docker Compose

1. **Подготовьте файлы в корне проекта**  
   - `.env` (см. образец ниже)  
   - `creds.json` (Google сервис‑аккаунт)  
   - SSL‑сертификаты в папке `ssl/` (Let’s Encrypt)

2. **Пример `.env`**  
   ```ini
   MODE=dev

   POSTGRES_USER=user1
   POSTGRES_PASSWORD=qwerty
   POSTGRES_HOST=postgres
   POSTGRES_PORT=5432
   POSTGRES_DB=table_reservations

   TELEGRAM_TOKEN=<ваш_токен>
   WEBHOOK_HOST=https://your-domain.com

   GOOGLE_SHEETS_CREDENTIALS=creds.json
   GOOGLE_SHEET_NAME=DataBridgeBot_table
   ```
   
3. **Запустите сборку и старт**

    ```bash
    docker-compose up --build -d
    ```

4. **Проверьте работу**
- В браузере: https://your-domain.com → Bot is running!

- В Telegram: отправьте /start, нажмите «Получить данные» и «Сохранить данные»