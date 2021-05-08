from dataclasses import dataclass
import os
from functools import wraps

import jsons

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


def _cached(function):
    """Cache the return value of a method in self.opened_games."""

    @wraps(function)
    def wrapped_function(self, id_):
        try:
            return self.opened_games[id_]
        except KeyError:
            game = function(self, id_)
            self.opened_games[id_] = game
            return game

    return wrapped_function


class GameStore:
    """A persistent store for Game instances."""

    def __init__(self, bot):
        self.bot = bot

        # TODO: Unload games when they are not in use
        self.opened_games = {}

    def _get_path(self, id_):
        """Return the path to the JSON file for an ID."""

        return self.bot.get_data_path(f"{id_}.json")

    @_cached
    def create(self, id_):
        """Create a new game."""

        return Game.new(id_)

    @_cached
    def load(self, id_):
        """Load a game from disk."""

        path = self._get_path(id_)

        try:
            with open(path) as file:
                json = file.read()
        except FileNotFoundError as error:
            raise KeyError(f"Game {id_} does not exist") from error

        return jsons.loads(json, Game)

    def save(self, game):
        """Write a game to disk."""

        json = jsons.dumps(game, strip_properties=True)
        path = self._get_path(game.id_)

        with open(path, "w") as file:
            file.write(json)

    def save_all(self):
        """Persist all opened games."""

        for game in self.opened_games.values():
            self.save(game)

    def delete(self, game):
        """Delete a game."""

        path = self._get_path(game.id_)
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

        del self.opened_games[game.id_]


def with_game(context):
    """
    A check which only permits commands within a game category.

    The game instance, if found, will be stored as context.game for easy access.
    """

    if context.channel.category is None:
        return False

    game_store = context.bot.get_cog("Game").game_store
    try:
        context.game = game_store.load(context.channel.category.id)
    except KeyError:
        return False

    return True
