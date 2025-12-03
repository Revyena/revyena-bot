import asyncpg
import settings
from database.pool import DBPool


class RevHandler:
    """
    A wrapper class for handling database queries through the connection pool.
    Uses pool.py to manage the connection pool.

    Methods:
        fetch(query: str, *args) -> list[asyncpg.Record]: Executes a SELECT query and returns the results.
        execute(query: str, *args) -> str: Executes an INSERT, UPDATE, or DELETE query and returns the status.
    """

    def __init__(self, pool: asyncpg.pool.Pool = None):
        self.pool = pool or DBPool().get_pool()

    async def fetch(self, query: str, *args) -> list[asyncpg.Record]:
        """
        Executes a SELECT query and returns the results.
        :param query: The SQL query to execute.
        :param args: The arguments to pass to the query.
        :return: A list of asyncpg.Record objects containing the query results.
        """
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetchrow(self, query: str, *args) -> asyncpg.Record | None:
        """
        Executes a SELECT query and returns a single row.
        :param query: The SQL query to execute.
        :param args: The arguments to pass to the query.
        :return: An asyncpg.Record object containing the query result, or None if no row is found.
        """
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def execute(self, query: str, *args):
        """
        Executes an INSERT, UPDATE, or DELETE query and returns the status.
        :param query: The SQL query to execute.
        :param args: The arguments to pass to the query.
        :return: The status of the executed query.
        """
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)