import os
from dotenv import load_dotenv

load_dotenv()

#######################################################################################
#                    Essential environment variables for bot setup                    #
#######################################################################################
BOT_TOKEN = os.getenv("BOT_TOKEN")
DEBUG_GUILDS = [int(guild) for guild in os.getenv("DEBUG_GUILDS", "").split(",")]

#######################################################################################
#                    Database configuration variables for bot                         #
#######################################################################################
DATABASE_HOST = os.getenv("POSTGRES_HOST", "localhost")
DATABASE_PORT = int(os.getenv("POSTGRES_PORT", 5432))
DATABASE_USER = os.getenv("POSTGRES_USER")
DATABASE_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE_NAME = os.getenv("POSTGRES_DB")

# If no explicit DATABASE_URL provided, construct one from the parts (if available)
if DATABASE_USER and DATABASE_PASSWORD and DATABASE_NAME:
    DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"