import logging
import asyncio

import discord

import settings
from database.pool import db_pool
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


async def main():
    await db_pool.init_pool()

    # Create bot instance
    bot = RevyenaBot(debug_guilds=settings.DEBUG_GUILDS)
    bot.revhandler = RevHandler(db_pool.get_pool())

    # Load extensions
    bot.load_extensions('modules', recursive=True)

    # Optional: log on_ready
    @bot.listen()
    async def on_ready():
        is_pool_initialized = '✅' if db_pool.get_pool() else '❌'
        are_extensions_loaded = '✅' if bot.extensions else '❌'
        is_revhandler_initialized = '✅' if bot.revhandler else '❌'
        bot.logger.info("Extension modules loading status: %s", are_extensions_loaded)
        bot.logger.info("Database pool initialisation status: %s", is_pool_initialized)
        bot.logger.info("RevHandler initialization status: %s", is_revhandler_initialized)
        if not is_pool_initialized or not are_extensions_loaded:
            bot.logger.error("The database pool is not initialized or extensions failed to load, shutting down.")
            await bot.close()
        bot.logger.info(f'Logged in as {bot.user} (ID: {bot.user.id})')

    # Run the bot
    await bot.start(settings.BOT_TOKEN, reconnect=True)


if __name__ == "__main__":
    asyncio.run(main())
