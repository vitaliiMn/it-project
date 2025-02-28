from fastapi import FastAPI

from services.producer import producer

from contextlib import asynccontextmanager

from routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await producer.start()
    yield
    await producer.stop()

app = FastAPI(lifespan=lifespan)

app.include_router(router)