import uvicorn
from fastapi import FastAPI, Depends

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio.client import Redis

from src.auth.service import current_active_user
from src.database.sql.alchemy_models import User
from src.database.sql.postgres_conn import database
from src.database.cache.redis_conn import cache_database

from src.image.routes import router as images
from src.auth.routes import router as auth
from src.comment.routes import router as comments

app = FastAPI()

app.include_router(auth)
app.include_router(images, prefix='/api')
app.include_router(comments, prefix='/api')


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/example/healthchecker")
async def healthchecker(db: AsyncSession = Depends(database), cache: Redis = Depends(cache_database)):
    print('postgres connection check...')
    await db.execute(text("SELECT 1"))
    print('redis connection check...')
    await cache.set("1", 1)
    return {"message": "Databases are OK!"}


@app.get("/example/user-authenticated")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8080)
