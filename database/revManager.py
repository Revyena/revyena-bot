from __future__ import annotations

from typing import TYPE_CHECKING

from database.tables import SCHEMA

if TYPE_CHECKING:
    from revyenaBot import RevyenaBot


class RevManager:
    def __init__(self, bot: RevyenaBot):
        self.tables = SCHEMA
        self.bot = bot

    async def create_schema(self):
        """
        Public method to initialize the schema definition.
        """
        self.bot.logger.info("Schema found with defined tables: %s", list(self.tables.keys()))
        self.bot.logger.info("Verifying and creating tables if they do not exist...")
        await self.bot.revhandler.ensure_schema(self.tables)
        self.bot.logger.info("Tables have been created or verified.")