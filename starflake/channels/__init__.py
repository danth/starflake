from abc import ABC, abstractmethod
from dataclasses import dataclass

import discord

from starflake.game_objects.game import Game


@dataclass(frozen=True)
class Channel(ABC):
    """A channel created during game setup."""

    category: discord.CategoryChannel
    game: Game

    @property
    @abstractmethod
    def name(self):
        """The channel name."""

    @property
    @abstractmethod
    def topic(self):
        """A concise description of the channel."""

    @property
    def overwrites(self):
        """A dictionary of discord.PermissionOverwrites for this channel."""

        return {}

    async def create(self, reason):
        """Create this channel."""

        return await self.category.create_text_channel(
            self.name,
            topic=self.topic,
            overwrites=self.overwrites,
            reason=reason,
        )


class DocumentChannel(Channel):
    """A read-only channel to which some messages are sent during setup."""

    @abstractmethod
    async def send_document(self, messageable):
        """Send the contents of the document."""

    @property
    def overwrites(self):
        return {
            self.category.guild.default_role: discord.PermissionOverwrite(
                send_messages=False, add_reactions=False, manage_messages=False
            ),
            self.category.guild.me: discord.PermissionOverwrite(
                send_messages=True, add_reactions=True, manage_messages=True
            ),
        }

    async def create(self, reason):
        channel = await super().create(reason)
        await self.send_document(channel)
        return channel
