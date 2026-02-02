from fastapi import FastAPI

from api import router

app = FastAPI()
app.include_router(router)


@app.get("/")
async def root():
    return {"msg": "Inventory Service is running", "docs": "/docs"}
