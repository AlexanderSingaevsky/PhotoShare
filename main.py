import uvicorn
from fastapi import FastAPI, Depends

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio.client import Redis

from src.database.sql.postgres_conn import database
from src.database.cache.redis_conn import cache_database

from src.image.routes import router as images
from src.auth.routes import router as auth

app = FastAPI()

app.include_router(images, prefix='/api')


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(database), cache: Redis = Depends(cache_database)):
    print('postgres connection check...')
    await db.execute(text("SELECT 1"))
    print('redis connection check...')
    await cache.set("1", 1)
    return {"message": "Databases are OK!"}

app.include_router(auth)


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8080)
