import logging
import os.path

import chickennuggets
import discord
import discordhealthcheck
from discord.ext import commands

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def launch():
    """Launch the Discord bot."""
    # Set up Discord bot
    logger.info("Setting up bot")
    bot = commands.Bot(command_prefix="+")

    # Load extensions
    logger.info("Loading extensions")
    chickennuggets.load(bot, ["help", "errors"])

    # Set up Docker health checks
    discordhealthcheck.start(bot)

    # Connect to Discord and start bot
    logger.info("Starting bot")
    bot.run(os.environ["DISCORD_TOKEN"])


if __name__ == "__main__":
    launch()
