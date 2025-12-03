import discord
from discord import ApplicationContext

from database.revhandler import RevHandler
from main import RevyenaBot
from utilities.modules.leveling import LevelingUtilities
from views.basicView import BasicImageView

# TODO: Add on_message handling for leveling system
# TODO: Fix progress bar calculation
# TODO: Add leaderboard command
# TODO: Add admin commands for managing leveling system
# TODO: Add XP decay or cooldowns to prevent farming
class LevelingCog(discord.Cog, name='Leveling'):
    def __init__(self, bot: RevyenaBot):
        self.bot = bot
        self.revhandler = RevHandler()

    leveling = discord.SlashCommandGroup(
        name='leveling',
        description='Commands related to the leveling system.'
        )

    @leveling.command(name='rank')
    async def rank(self, ctx: ApplicationContext):
        user_level = await self.bot.revhandler.fetch('SELECT level, xp FROM user_levels WHERE user_id = $1', ctx.user.id)
        if not user_level:
            await ctx.respond("You don't have any XP or levels yet. Start participating to earn XP!")
            return

        xp = user_level[0]['xp']

        level = LevelingUtilities.level_from_xp(xp)
        progress = LevelingUtilities.progress_to_next_level(xp)

        # Build a simple text progress bar !!! THIS DOESNT CALCULATE CORRECTLY YET
        bar_length = 20
        filled_length = int(progress * bar_length)
        bar = "█" * filled_length + "—" * (bar_length - filled_length)

        message_content = (
            f"**{ctx.user.display_name}'s Rank**\n"
            f"Level: {level}\n"
            f"XP: {xp} / {LevelingUtilities.calculate_experience(level + 1)}\n"
            f"Progress: [{bar}] {int(progress * 100)}%\n"
            f"Rank: #42 (placeholder)"
        )

        await ctx.respond(
            view=BasicImageView(
                description=message_content,
                avatar_url=ctx.user.display_avatar.url
            )
        )

def setup(bot):
    bot.add_cog(LevelingCog(bot))