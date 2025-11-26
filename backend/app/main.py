from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import ping, health, clients, applications, auth
from app.auth.seed import seed_admin
from app.core.config import settings
from app.db.init_db import init_db

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    seed_admin()
    yield


app = FastAPI(title="СОК (MVP)", lifespan=lifespan)

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
app.include_router(auth.router, prefix="/api")
