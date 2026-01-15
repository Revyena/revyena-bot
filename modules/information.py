import discord

from revyenaBot import RevyenaBot
from utilities.modules.information import InformationUtilities
from views.basicView import BasicImageView


class InformationCog(discord.Cog, name="Information"):
    def __init__(self, bot: RevyenaBot):
        self.bot = bot
        self.utilities = InformationUtilities()


    @discord.slash_command(name="information")
    async def info(self, ctx):
        """Provides information about the bot and its statistics."""
        latency = round(self.bot.latency * 1000)
        hardware_info = self.utilities.get_hardware_usage_info()
        python_info = self.utilities.get_python_info()
        module_list = '\n- '.join(self.bot.cogs.keys())

        message_content = f"""
# About
{self.bot.user.display_name} was created to assist in management of servers and communities. Aimed primarily to serve the Mamono community, \
it offers a variety of features including moderation tools, event scheduling, and user engagement functionalities, as well \
as fun commands to enhance interaction within the server and detailed logging.

**Python Version:** {python_info["python_version"]}
## Statistics
**Users:** {len(self.bot.users)}
**API Latency:** {latency}ms
**RAM:** {hardware_info["ram_used"]}GB used out of {hardware_info["ram_total"]}GB total ({hardware_info["ram_used_percent"]}% used)
**Disk:** {hardware_info["disk_free"]}GB free out of {hardware_info["disk_total"]}GB total ({hardware_info["disk_free_percent"]}% free)
## Modules
- {module_list}
        """
        return await ctx.respond(
            view=BasicImageView(
            description=message_content,
            avatar_url=self.bot.user.avatar.url
            )
        )


def setup(bot):
    bot.add_cog(InformationCog(bot))
