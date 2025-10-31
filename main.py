import discord
from discord.ext import commands

import settings


class RevyenaBot(commands.Bot):
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

    async def on_connect(self):
        print("Setup complete. You can load cogs or sync commands here.")

    async def on_ready(self):
        print(f"✅ Logged in as {self.user} (ID: {self.user.id})")


if __name__ == "__main__":
    bot = RevyenaBot(debug_guilds=settings.DEBUG_GUILDS)
    bot.run(settings.BOT_TOKEN)
