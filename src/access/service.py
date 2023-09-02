from typing import List

from fastapi import Request, Depends, HTTPException, status

from src.database.sql.alchemy_models import User
from redis.asyncio.client import Redis
from src.database.cache.redis_conn import cache_database
from src.auth.service import current_active_user


class AccessService:
    def __init__(self, action: str):
        self.action = action

    async def __call__(self, request: Request,
                       user: User = Depends(current_active_user),
                       cache: Redis = Depends(cache_database)):
        return None

