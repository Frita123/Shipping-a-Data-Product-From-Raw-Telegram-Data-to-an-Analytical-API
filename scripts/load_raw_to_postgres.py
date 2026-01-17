

import os
import json
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
#DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", 5432)
DB_NAME = os.getenv("POSTGRES_DB", "medical_db")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "postgres")


conn = psycopg2.connect(
    host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS
)
cur = conn.cursor()

# Create table if not exists
cur.execute("""
CREATE TABLE IF NOT EXISTS raw.telegram_messages (
    message_id BIGINT PRIMARY KEY,
    channel_name TEXT,
    message_date TIMESTAMP,
    message_text TEXT,
    has_media BOOLEAN,
    image_path TEXT,
    views INT,
    forwards INT
)
""")
conn.commit()

# Load JSON files
base_path = "data/raw/telegram_messages"
for date_folder in os.listdir(base_path):
    folder_path = os.path.join(base_path, date_folder)
    if os.path.isdir(folder_path):
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".json"):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, "r", encoding="utf-8") as f:
                    messages = json.load(f)
                    for msg in messages:
                        cur.execute("""
                        INSERT INTO raw.telegram_messages (
                            message_id, channel_name, message_date, message_text,
                            has_media, image_path, views, forwards
                        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                        ON CONFLICT (message_id) DO NOTHING
                        """, (
                            msg.get("message_id"),
                            msg.get("channel_name"),
                            msg.get("date"),
                            msg.get("text"),
                            msg.get("has_media"),
                            msg.get("image_path"),
                            msg.get("views"),
                            msg.get("forwards")
                        ))
conn.commit()
cur.close()
conn.close()
print("Raw data loaded into PostgreSQL successfully!")
