from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .db import connect_to_mongo, close_mongo_connection
from .realtime.websocket import manager
from .routers.endpoints import router as api_router
from .routers.chat import router as chat_router
from .seed import seed

app = FastAPI(title="Logistics Dispatcher")

origins = [o.strip() for o in settings.allowed_origins.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.include_router(chat_router)


@app.on_event("startup")
async def on_startup():
    await connect_to_mongo()
    await seed()


@app.on_event("shutdown")
async def on_shutdown():
    await close_mongo_connection()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # We can echo pings or ignore received messages
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)