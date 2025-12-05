import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", '')

BOT_TOKEN = os.getenv("BOT_TOKEN", '')

DATABASE_URL = os.getenv("DATABASE_URL", 'sqlite:///telegram_monitor.db')

DEFAULT_MIN_REACTIONS = 1000
