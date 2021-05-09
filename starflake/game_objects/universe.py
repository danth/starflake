import os
from dataclasses import dataclass
from functools import wraps

import jsons

from starflake.game_objects import RandomisableGameObject
from starflake.game_objects.periodic_table import PeriodicTable


@dataclass(frozen=True)
class Universe(RandomisableGameObject):
    """Data relating to an individual game."""

    id_: int
    periodic_table: PeriodicTable

    @classmethod
    def random(cls, id_):
        """Generate a new universe with the given ID."""

        periodic_table = PeriodicTable.random()

        return cls(id_, periodic_table)


def _cached(function):
    """Cache the return value of a method in self.opened_universes."""

    @wraps(function)
    def wrapped_function(self, id_):
        try:
            return self.opened_universes[id_]
        except KeyError:
            universe = function(self, id_)
            self.opened_universes[id_] = universe
            return universe

    return wrapped_function


class UniverseStore:
    """A persistent store for Universe instances."""

    def __init__(self, bot):
        self.bot = bot

        # TODO: Unload universes when they are not in use
        self.opened_universes = {}

    def _get_path(self, id_):
        """Return the path to the JSON file for an ID."""

        return self.bot.get_data_path(f"{id_}.json")

    @_cached
    def create(self, id_):
        """Create a new universe."""

        return Universe.random(id_)

    @_cached
    def load(self, id_):
        """Load a universe from disk."""

        path = self._get_path(id_)

        try:
            with open(path) as file:
                json = file.read()
        except FileNotFoundError as error:
            raise KeyError(f"Universe {id_} does not exist") from error

        return jsons.loads(json, Universe)

    def save(self, universe):
        """Write a universe to disk."""

        json = jsons.dumps(universe, strip_properties=True)
        path = self._get_path(universe.id_)

        with open(path, "w") as file:
            file.write(json)

    def save_all(self):
        """Persist all opened universes."""

        for universe in self.opened_universes.values():
            self.save(universe)

    def delete(self, universe):
        """Delete a universe."""

        path = self._get_path(universe.id_)
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

        del self.opened_universes[universe.id_]


def with_universe(context):
    """
    A check which only permits commands within a universe.

    The universe instance, if found, will be stored as context.universe for easy access.
    """

    if context.channel.category is None:
        return False

    universe_store = context.bot.get_cog("Universe").universe_store
    try:
        context.universe = universe_store.load(context.channel.category.id)
    except KeyError:
        return False

    return True
