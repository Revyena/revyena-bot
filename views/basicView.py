import discord

class BasicImageView(discord.ui.DesignerView):
    def __init__(self, description: str, avatar_url: str = None):
        components = discord.ui.Container(
            discord.ui.TextDisplay(description) if not avatar_url else
            discord.ui.Section(
                discord.ui.TextDisplay(description),
                accessory=discord.ui.Thumbnail(url=avatar_url)
            )
        )

        super().__init__(components)
