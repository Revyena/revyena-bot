import discord
from discord import ApplicationContext

from revyenaBot import RevyenaBot
from utilities.modules.leveling import LevelingRepository, LevelingMath
from views.basicView import BasicImageView


# TODO: Add leaderboard command
# TODO: Add admin commands for managing leveling system
# TODO: Add XP decay or cooldowns to prevent farming
class LevelingCog(discord.Cog, name='Leveling'):
    def __init__(self, bot: RevyenaBot):
        self.bot = bot

    leveling = discord.SlashCommandGroup(
        name='leveling',
        description='Commands related to the leveling system.'
        )

    @leveling.command(name='rank')
    async def rank(self, ctx: ApplicationContext):
        user = await LevelingRepository.get_experience(user_id=ctx.author.id, guild_id=ctx.guild.id, bot=self.bot)
        if not user or not user.experience:
            await ctx.respond("You don't have any XP or levels yet. Start participating to earn XP!", ephemeral=True)
            return

        level = LevelingMath.level_from_xp(experience=user.experience)
        experience_next_level = LevelingMath.xp_to_next_level(experience=user.experience)

        message_content=f"""
## {ctx.user.display_name}: Level {level}
**Total experience:** `{user.experience}` XP
**XP to next level:** `{experience_next_level}` XP
        """

        await ctx.respond(
            view=BasicImageView(
                description=message_content,
                avatar_url=ctx.user.display_avatar.url
            )
        )

    @leveling.command(name='leaderboard')
    async def leaderboard(self, ctx: ApplicationContext):
        leaderboard_rows = await LevelingRepository.get_leaderboard(guild_id=ctx.guild.id, limit=10, bot=self.bot)
        if not leaderboard_rows:
            await ctx.respond("No XP data found for this server.", ephemeral=True)
            return

        description_lines = []
        for rank, row in enumerate(leaderboard_rows, start=1):
            user = await self.bot.fetch_user(row.user_id)
            level = LevelingMath.level_from_xp(experience=row.experience)
            description_lines.append(f"**{rank}. {user.display_name}** – Level {level} ({row.experience} XP)")

        message_content = chr(10).join(description_lines)

        print(
            "description_lines: ", description_lines,
            "message_content: ", message_content
        )

        await ctx.respond(
            view=BasicImageView(
                description=message_content
            )
        )


def setup(bot):
    bot.add_cog(LevelingCog(bot))
