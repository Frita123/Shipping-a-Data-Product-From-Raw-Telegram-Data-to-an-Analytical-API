from sqlalchemy.orm import Session
from sqlalchemy import text

# 1. Top Products
def get_top_products(db: Session, limit: int):
    query = text("""
        SELECT word AS term, COUNT(*) AS count
        FROM raw.fct_messages,
             unnest(string_to_array(lower(message_text), ' ')) AS word
        GROUP BY word
        ORDER BY count DESC
        LIMIT :limit
    """)
    return db.execute(query, {"limit": limit}).fetchall()

# 2. Channel Activity
def get_channel_activity(db: Session, channel_name: str):
    query = text("""
        SELECT c.channel_name, COUNT(*) AS total_messages
        FROM raw.fct_messages m
        JOIN raw.dim_channels c ON m.channel_key = c.channel_key
        WHERE c.channel_name ILIKE :channel
        GROUP BY c.channel_name
    """)
    return db.execute(query, {"channel": f"%{channel_name}%"}).fetchall()

# 3. Message Search
def search_messages(db: Session, query_text: str, limit: int):
    query = text("""
        SELECT message_id, message_text
        FROM raw.fct_messages
        WHERE message_text ILIKE :q
        LIMIT :limit
    """)
    return db.execute(query, {"q": f"%{query_text}%", "limit": limit}).fetchall()

# 4. Visual Content Stats
def visual_content_stats(db: Session):
    query = text("""
        SELECT image_category, COUNT(*) AS total_images
        FROM raw.fct_image_detections
        GROUP BY image_category
    """)
    return db.execute(query).fetchall()
