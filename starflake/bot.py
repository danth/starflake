import logging
import os.path
import pickle

import chickennuggets
import discordhealthcheck
from discord.ext import commands

from starflake.game_objects.periodic_table import PeriodicTable

logger = logging.getLogger(__name__)


class StarflakeBot(commands.Bot):
    def __init__(self, directory, token):
        super().__init__(command_prefix="+")
        self.directory = directory
        self.token = token

        logger.info("Starting health check")
        discordhealthcheck.start(self)

        logger.info("Loading cogs")
        chickennuggets.load(self, ["help", "errors"])
        self.load_extension("starflake.cogs.game")
        self.load_extension("starflake.cogs.information")

    def run(self):
        super().run(self.token)

    def get_data_path(self, path):
        """Return the absolute path to a data file."""

        return os.path.join(self.directory, path)
