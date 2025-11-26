from dotenv import load_dotenv
from fastapi import FastAPI
from app.api import ping, health

load_dotenv()

app = FastAPI(title="СОК (MVP)")

# Префикс /api, чтобы потом не путаться с фронтом/nginx
app.include_router(ping.router, prefix="/api")
app.include_router(health.router, prefix="/api")
