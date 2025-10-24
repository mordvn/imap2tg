# IMAP to Telegram Bot

Telegram bot for forwarding emails from IMAP to a specified Telegram chat. Built with Python 3.13, Aiogram 3, and IMAP.

<img src="images/example-image.png" alt="Example Image" width="300">

🚀 Features

- Автоматическая проверка новых писем
- Пересылка текстового содержимого писем
- Пересылка вложений
- Поддержка HTML-форматирования
- Автоматическое декодирование тем писем
- Обработка ошибок и повторные попытки

📦 Установка и запуск

1. Клонируйте репозиторий:

```bash
git clone https://github.com/mordvn/imap2tg.git
cd imap2tg
```

2. Создайте файл .env с настройками:

```env
# Email settings
MAIL_USERNAME=youremail@mail.ru
MAIL_PASSWORD=yourpassword
MAIL_SERVER=imap.mail.ru

# Telegram settings
BOT_TOKEN=your_bot_token
CHAT_ID=your_chat_id

# Application settings
CHECK_INTERVAL=300
RETRY_INTERVAL=60
```

3. Установите зависимости (используя UV):

```bash
# Установка UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Установить зависимости
python -m pip install uv
uv sync --frozen
```

4. Запустите бота:

```bash
uv run python3 app/main.py
```

3-4 Используя Docker:

```bash
docker build -t imap2tg .
docker run -d --name imap2tg imap2tg
```

## Разработчики

Разработано для группы БПИ23-01 университета СибГУ
