import logging
import time
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import ping, health, clients, applications, auth
from app.auth.seed import seed_admin
from app.core.config import settings
from app.core.errors import validation_errors_to_list
from app.core.logging_config import setup_logging
from app.db.init_db import init_db

load_dotenv()
setup_logging()
log = logging.getLogger("sok")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    seed_admin()
    yield


app = FastAPI(title="СОК (MVP)", lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Логирование каждого запроса
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    try:
        response = await call_next(request)
        return response
    finally:
        ms = (time.perf_counter() - start) * 1000
        log.info("%s %s -> %.1fms", request.method, request.url.path, ms)


# Единый формат валидационных ошибок (по гайду FastAPI) :contentReference[oaicite:1]{index=1}
@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": validation_errors_to_list(exc.errors()),
        },
    )


app.include_router(ping.router, prefix="/api")
app.include_router(health.router, prefix="/api")
app.include_router(clients.router, prefix="/api")
app.include_router(applications.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
