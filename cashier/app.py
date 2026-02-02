from contextlib import asynccontextmanager

from fastapi import FastAPI

from api import router
from core.broker import broker


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broker.connect()
    yield
    await broker.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router)


@app.get("/")
async def root():
    return {"msg": "Order Service is running", "docs": "/docs"}
