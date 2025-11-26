from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from app.api import ping, health, clients, applications
from app.db.init_db import init_db

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="СОК (MVP)", lifespan=lifespan)

app.include_router(ping.router, prefix="/api")
app.include_router(health.router, prefix="/api")
app.include_router(clients.router, prefix="/api")
app.include_router(applications.router, prefix="/api")
