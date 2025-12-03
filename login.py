from telethon import TelegramClient
from config import API_ID, API_HASH
import asyncio


async def login():
    print("🔐 Авторизация Telethon...")

    client = TelegramClient('monitor_session', API_ID, API_HASH)
    await client.start()

    print("✅ Готово! Теперь запускай бота командой: python bot.py")
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(login())
