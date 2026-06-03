import sys
import asyncio
import json
from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
import redis.asyncio as aioredis

from database import get_db, engine, Base
from models import Poll, Choice
from schemas import PollCreate, VoteCreate, PollResponse

app = FastAPI(title="Real-Time Polling Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REDIS_URL = "redis://localhost:6379"
redis_client = None

@app.on_event("startup")
async def startup():
    global redis_client
    redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    if redis_client:
        await redis_client.close()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass

manager = ConnectionManager()

async def redis_listener():
    pubsub = redis_client.pubsub()
    await pubsub.subscribe("poll_updates")
    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                await manager.broadcast(message["data"])
    except asyncio.CancelledError:
        await pubsub.unsubscribe("poll_updates")

@app.on_event("startup")
async def start_redis_listener():
    asyncio.create_task(redis_listener())

@app.post("/polls", response_model=PollResponse)
async def create_poll(poll_data: PollCreate, db: AsyncSession = Depends(get_db)):
    new_poll = Poll(title=poll_data.title)
    db.add(new_poll)
    await db.flush()
    
    for text in poll_data.choices:
        choice = Choice(text=text, poll_id=new_poll.id)
        db.add(choice)
        
    await db.commit()
    await db.refresh(new_poll)
    return new_poll

@app.get("/polls", response_model=list[PollResponse])
async def get_polls(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Poll))
    return result.scalars().unique().all()

@app.post("/votes")
async def cast_vote(vote: VoteCreate, db: AsyncSession = Depends(get_db)):
    redis_key = f"poll:{vote.poll_id}:voters"
    is_new_voter = await redis_client.sadd(redis_key, vote.voter_fingerprint)
    
    if not is_new_voter:
        raise HTTPException(status_code=400, detail="You have already voted on this poll.")
    
    stmt = (
        update(Choice)
        .where(Choice.id == vote.choice_id, Choice.poll_id == vote.poll_id)
        .values(votes=Choice.votes + 1)
    )
    await db.execute(stmt)
    await db.commit()
    
    result = await db.execute(select(Poll).where(Poll.id == vote.poll_id))
    updated_poll = result.scalars().unique().one()
    
    payload = {
        "poll_id": updated_poll.id,
        "choices": [{"id": c.id, "text": c.text, "votes": c.votes} for c in updated_poll.choices]
    }
    await redis_client.publish("poll_updates", json.dumps(payload))
    
    return {"status": "success", "message": "Vote processed successfully."}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("index.html", "r") as f:
        return f.read()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, loop="asyncio")