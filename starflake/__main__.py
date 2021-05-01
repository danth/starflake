import logging
import os

from starflake.bot import StarflakeBot


def launch():
    """Launch the Discord bot."""

    logging.basicConfig(level=logging.INFO)

    bot = StarflakeBot(
        os.environ["STARFLAKE_DIR"],
        os.environ["DISCORD_TOKEN"],
    )
    bot.run()


if __name__ == "__main__":
    launch()
