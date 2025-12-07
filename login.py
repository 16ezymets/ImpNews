from telethon import TelegramClient
from config import API_ID, API_HASH
import asyncio


async def login():
    print("🔐 Telethon authorisation...")

    client = TelegramClient('monitor_session', API_ID, API_HASH)
    await client.start()

    print("✅ Done! Now launch the bot: python bot.py")
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(login())
