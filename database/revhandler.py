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

    async def _create_table(self, name: str, columns: dict, constraints: list[str] = None):
        """
        Create a table using a simple Python definition.

        columns: {
            "user_id": "BIGINT PRIMARY KEY",
            "xp": "INT NOT NULL DEFAULT 0"
        }

        constraints: ["UNIQUE(user_id, xp)"]
        """
        column_sql = ",\n    ".join(f"{col} {defn}" for col, defn in columns.items())
        constraints_sql = ""

        if constraints:
            constraints_sql = ",\n    " + ",\n    ".join(constraints)

        query = f"""
        CREATE TABLE IF NOT EXISTS {name} (
            {column_sql}{constraints_sql}
        );
        """

        async with self.pool.acquire() as conn:
            await conn.execute(query)

    async def ensure_schema(self, schema: dict):
        """
        schema = {
            "user_levels": {
                "columns": {...},
                "constraints": [...]
            },
            "profiles": {...}
        }
        """
        for table_name, spec in schema.items():
            await self._create_table(
                table_name,
                spec["columns"],
                spec.get("constraints")
            )