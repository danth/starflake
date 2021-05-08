from abc import ABC, abstractmethod


class GameObject(ABC):
    """A serialisable object which stores game data."""


class RandomisableGameObject(GameObject):
    """A game object which can be generated at random."""

    @classmethod
    @abstractmethod
    def random(cls, *args):
        """Instantiate a random object."""


class EmbeddableGameObject(GameObject):
    """A game object which is presentable to users through a discord.Embed."""

    @abstractmethod
    async def send_embed(self, messageable):
        """Send a representation of this object to the given channel."""


class BondingException(Exception):
    pass


class BondableGameObject(GameObject):
    """A game object which is able to bond with other instances of itself."""

    @abstractmethod
    def can_bond(self, other):
        """Return whether these two objects are able to bond."""

    @abstractmethod
    def bond(self, other):
        """
        Bond these two objects.

        Does not include any sanity checks.
        """

    def __add__(self, other):
        """
        Bond these two objects.

        Raises BondingException if the objects are not allowed to bond.
        """

        if not self.can_bond(other):
            raise BondingException(f"{self} cannot be bonded to {other}")

        return self.bond(other)

    @staticmethod
    def bond_many(objects):
        """
        Bond this collection of objects.

        Raises BondingException if any of the objects are not allowed to bond.
        """

        if not objects:
            # An empty collection was given
            return []

        final_object = objects[0]
        for object_ in objects[1:]:
            final_object += object_
        return final_object
