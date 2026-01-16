import os
import json
import logging
from datetime import datetime
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv

# Load secrets
load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Channels to scrape
CHANNELS = [
    "lobelia4cosmetics",
    "tikvahpharma"
]

# Output folders
BASE_DATA_PATH = "data/raw"
MESSAGE_PATH = os.path.join(BASE_DATA_PATH, "telegram_messages")
IMAGE_PATH = os.path.join(BASE_DATA_PATH, "images")

os.makedirs(MESSAGE_PATH, exist_ok=True)
os.makedirs(IMAGE_PATH, exist_ok=True)

client = TelegramClient("session", API_ID, API_HASH)

def save_messages(channel_name, messages):
    today = datetime.now().strftime("%Y-%m-%d")
    folder = os.path.join(MESSAGE_PATH, today)
    os.makedirs(folder, exist_ok=True)

    file_path = os.path.join(folder, f"{channel_name}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

    logging.info(f"Saved {len(messages)} messages for {channel_name}")

async def scrape_channel(channel_name):
    logging.info(f"Scraping channel: {channel_name}")

    messages_data = []

    async for message in client.iter_messages(channel_name, limit=500):
        msg = {
            "message_id": message.id,
            "date": message.date.isoformat() if message.date else None,
            "text": message.text,
            "views": message.views,
            "forwards": message.forwards,
            "has_media": message.media is not None,
            "image_path": None
        }

        # Download image if exists
        if message.photo:
            channel_folder = os.path.join(IMAGE_PATH, channel_name)
            os.makedirs(channel_folder, exist_ok=True)

            image_file = os.path.join(channel_folder, f"{message.id}.jpg")
            await message.download_media(file=image_file)
            msg["image_path"] = image_file

        messages_data.append(msg)

    save_messages(channel_name, messages_data)

async def main():
    await client.start()
    for channel in CHANNELS:
        try:
            await scrape_channel(channel)
        except Exception as e:
            logging.error(f"Error scraping {channel}: {e}")

    await client.disconnect()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
