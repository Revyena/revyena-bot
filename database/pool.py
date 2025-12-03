import asyncpg

import settings


class DBPool:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DBPool, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):  # Ensure pool is initialized only once
            self.pool = None
            self.initialized = False

    async def init_pool(self):
        if not self.initialized:
            self.pool = await asyncpg.create_pool(settings.DATABASE_URL)
            self.initialized = True

    async def close_pool(self):
        if self.pool:
            await self.pool.close()
            self.pool = None
            self.initialized = False

    def get_pool(self):
        return self.pool


# Instantiate and export a single instance
db_pool = DBPool()