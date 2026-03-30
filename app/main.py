import sys
from pathlib import Path

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes import ride
from app.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    init_db()
    yield
    # 关闭时执行（如果需要）

app = FastAPI(title="Bike Ride Service API", version="1.0.0", lifespan=lifespan)
app.include_router(ride.router, prefix="/ride", tags=["rides"])