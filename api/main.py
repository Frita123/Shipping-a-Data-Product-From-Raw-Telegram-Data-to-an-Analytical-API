from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from api.database import SessionLocal
from api import crud

app = FastAPI(
    title="Medical Telegram Analytics API",
    description="Analytical API for Telegram medical channels",
    version="1.0"
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------
# Endpoint 1: Top Products
# -----------------------
@app.get("/api/reports/top-products")
def top_products(limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_top_products(db, limit)

# -----------------------
# Endpoint 2: Channel Activity
# -----------------------
@app.get("/api/channels/{channel_name}/activity")
def channel_activity(channel_name: str, db: Session = Depends(get_db)):
    result = crud.get_channel_activity(db, channel_name)
    if not result:
        raise HTTPException(status_code=404, detail="Channel not found")
    return result

# -----------------------
# Endpoint 3: Message Search
# -----------------------
@app.get("/api/search/messages")
def search_messages(query: str, limit: int = 20, db: Session = Depends(get_db)):
    return crud.search_messages(db, query, limit)

# -----------------------
# Endpoint 4: Visual Content Stats
# -----------------------
@app.get("/api/reports/visual-content")
def visual_content(db: Session = Depends(get_db)):
    return crud.visual_content_stats(db)
