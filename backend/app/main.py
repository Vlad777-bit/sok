from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import ping, health, clients, applications
from app.core.config import settings
from app.db.init_db import init_db

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="СОК (MVP)", lifespan=lifespan)

# CORS: разрешаем фронту ходить на API из браузера
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ping.router, prefix="/api")
app.include_router(health.router, prefix="/api")
app.include_router(clients.router, prefix="/api")
app.include_router(applications.router, prefix="/api")
