import asyncio
import sys
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

# Windows specific event loop override to permanently fix "Event loop is closed" crash
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(title="Real-Time Polling Engine")

# CORS Middleware (To prevent any connection block from frontend browser)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dummy/Global Connection Manager for WebSockets
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

# --- API ROUTES ---

@app.get("/health")
async def health_check():
    return {"status": "running", "engine": "FastAPI Asynchronous Pipeline"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keeps the socket connection alive and listens for incoming updates
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return """
        <html>
            <body style='font-family: sans-serif; text-align: center; padding-top: 50px;'>
                <h2>⚡ Real-Time Polling Engine Backend is Running!</h2>
                <p style='color: red;'>index.html file not found in the root directory.</p>
            </body>
        </html>
        """

# --- EXPLICIT PROGRAMMATIC STARTUP HARNESS ---
if __name__ == "__main__":
    import uvicorn
    # Enforcing 'selector' loop dynamically via execution parameters
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
    
