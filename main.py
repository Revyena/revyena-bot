import asyncio
from datetime import datetime, timezone

import discord

import settings
from database.pool import db_pool
from database.revhandler import RevHandler
from database.revManager import RevManager
from revyenaBot import RevyenaBot
from utilities.modules.leveling import LevelingRepository, LevelingService


async def main():
    await db_pool.init_pool()

    # Create bot instance
    bot = RevyenaBot(debug_guilds=settings.DEBUG_GUILDS)
    bot.revhandler = RevHandler(db_pool.get_pool())

    # In-memory cooldowns to prevent XP farming: {(guild_id, user_id): last_awarded_timestamp}
    bot._xp_cooldowns = {}
    # XP settings
    bot._xp_per_message = getattr(settings, "XP_PER_MESSAGE", 25)
    bot._xp_cooldown_seconds = getattr(settings, "XP_COOLDOWN_SECONDS", 60)

    # Load extensions
    bot.load_extensions('modules', recursive=True)

    # Optional: log on_ready
    @bot.listen()
    async def on_ready():
        manager = RevManager(bot)
        await bot.revyena_ready(db_pool, manager)

    @bot.listen()
    async def on_message(message: discord.Message):
        if message.author.bot or message.guild is None:
            return

        user_id = message.author.id
        guild_id = message.guild.id
        user = await LevelingRepository.get_experience(user_id=user_id, guild_id=guild_id, bot=bot)  # load from DB

        reward_xp = LevelingService.can_award_xp(user, message)
        if not reward_xp:
            return

        result = LevelingService.apply_xp_on_message(current_xp=user.experience)

        await LevelingRepository.set_experience(user_id=user_id, guild_id=guild_id, experience=result.new_xp, bot=bot)

        if result.leveled_up:
            await message.channel.send(
                f"🎉 {message.author.mention} reached **Level {result.new_level}**!"
            )
    # Run the bot
    await bot.start(settings.BOT_TOKEN, reconnect=True)


if __name__ == "__main__":
    asyncio.run(main())
