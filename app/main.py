from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.database import Base, engine
from app.users.routers import router as user_router
import app.users.models
import app.products.models


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        #await conn.run_sync(Base.metadata.drop_all)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
@app.get('/')
async def hello():
    return 'hello world'

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)