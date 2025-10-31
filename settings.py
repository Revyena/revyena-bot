import os

from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
DEBUG_GUILDS = [int(guild) for guild in os.getenv("DEBUG_GUILDS", "").split(",")]