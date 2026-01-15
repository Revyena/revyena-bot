from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import discord

if TYPE_CHECKING:
    from database.pool import DBPool
    from database.revManager import RevManager
    from database.revhandler import RevHandler


class RevyenaBot(discord.Bot):
    def __init__(self, debug_guilds: list[int]):
        """
        A custom class for the Revyena bot.  Extends the commands.Bot class
        :param debug_guilds: A list of guilds with which slash commands should be synchronised
        """
        intents = discord.Intents.all()
        super().__init__(
            intents=intents,
            allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=False),
        )

        self.debug_guilds = debug_guilds

        self.logger = logging.getLogger("revyena")
        self.logger.setLevel(logging.INFO)

        # Only add a handler if not already added (prevents duplication)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("[%(levelname)s - %(asctime)s] %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        self.bot = self
        self.revhandler: RevHandler | None = None  # placeholder for RevHandler

    async def revyena_ready(self, db_pool: DBPool, manager: RevManager) -> None:
        """
        A custom ready event to be called when the bot is fully ready.
        """
        is_pool_initialized = '✅' if db_pool.get_pool() else '❌'
        are_extensions_loaded = '✅' if self.bot.extensions else '❌'
        is_revhandler_initialized = '✅' if self.bot.revhandler else '❌'
        self.bot.logger.info("-" * 40)
        self.bot.logger.info("Extension modules loading status: %s", are_extensions_loaded)
        self.bot.logger.info("Database pool initialisation status: %s", is_pool_initialized)
        self.bot.logger.info("RevHandler initialization status: %s", is_revhandler_initialized)
        if not is_pool_initialized or not are_extensions_loaded or not is_revhandler_initialized:
            self.bot.logger.error("The database pool is not initialized or extensions failed to load, shutting down.")
            await self.bot.close()
        self.bot.logger.info("-" * 40)
        await manager.create_schema()
        self.bot.logger.info("-" * 40)
        self.bot.logger.info(f'Logged in as {self.bot.user} (ID: {self.bot.user.id})')

