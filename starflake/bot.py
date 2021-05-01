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

        logger.info("Preparing periodic table")
        self._prepare_periodic_table()

        logger.info("Loading cogs")
        chickennuggets.load(self, ["help", "errors"])
        self.load_extension("starflake.cogs.information")

    def run(self):
        super().run(self.token)

    def _prepare_periodic_table(self):
        """Load or generate a periodic table."""

        periodic_table_path = self._get_path("periodic_table.pickle")
        if os.path.exists(periodic_table_path):

            with open(periodic_table_path, "rb") as periodic_table_file:
                self.periodic_table = pickle.load(periodic_table_file)

            logger.info("Loaded an existing periodic table:\n%s", self.periodic_table)

        else:
            self.periodic_table = PeriodicTable.random()

            with open(periodic_table_path, "wb") as periodic_table_file:
                pickle.dump(self.periodic_table, periodic_table_file)

            logger.info("Generated a new periodic table:\n%s", self.periodic_table)

    def _get_path(self, path):
        """Return the absolute path to a data file."""

        return os.path.join(self.directory, path)
