# IMAP to Telegram Bot

Telegram bot for forwarding emails from IMAP to a specified Telegram chat. Built with Python 3.13, Aiogram 3, and IMAP.

<img src="images/example-image.png" alt="Example Image" width="300">

🚀 Features

— Automatic checking for new emails
— Forwarding of email text content
— Forwarding of attachments
— Support for HTML formatting
— Automatic decoding of email subjects
— Error handling and retry mechanism

📦 Installation and Run

1. Clone the repository:

```bash
git clone https://github.com/mordvn/imap2tg.git
cd imap2tg
```

2. Create a .env file with configuration:

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

3. Install dependencies (using UV):

```bash
# Установка UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Установить зависимости
python -m pip install uv
uv sync --frozen
```

4. Run the bot:

```bash
uv run python3 app/main.py
```

3-4 Using Docker:

```bash
docker build -t imap2tg .
docker run -d --name imap2tg imap2tg
```

## License

MIT License

---
Developed for group BPI23-01 at Siberian State University (SibSAU).
