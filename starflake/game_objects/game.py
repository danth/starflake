import jsons
from dataclasses import dataclass

from starflake.game_objects.periodic_table import PeriodicTable


@dataclass(frozen=True)
class Game:
    """Data relating to an individual game."""

    id_: int
    periodic_table: PeriodicTable

    @classmethod
    def new(cls, id_):
        """Initialise a new game with the given ID."""

        periodic_table = PeriodicTable.random()

        return cls(id_, periodic_table)

    @classmethod
    def load(cls, bot, id_):
        """Load a game from disk."""

        path = bot.get_data_path(f"{id_}.json")
        with open(path, "r") as file:
            return jsons.loads(file.read(), cls)

    def save(self, bot):
        """Persist game data to disk."""

        path = bot.get_data_path(f"{self.id_}.json")
        with open(path, "w") as file:
            file.write(jsons.dumps(self, strip_properties=True))


def with_game(context):
    """
    A check which only permits commands within a game category.

    The game instance, if found, will be stored as context.game for easy access.
    """

    if context.channel.category is None:
        return False

    try:
        context.game = Game.load(context.bot, context.channel.category.id)
    except FileNotFoundError:
        return False

    return True
