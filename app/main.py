from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from app.users.routers import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)


@app.get("/")
async def hello():
    return "hello world"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
