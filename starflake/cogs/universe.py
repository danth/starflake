import asyncio

import discord
import jsons
from discord.ext import commands, tasks

from starflake.channels.commands import CommandsChannel
from starflake.channels.lore import LoreChannel
from starflake.game_objects.universe import UniverseStore, with_universe


class UniverseCog(commands.Cog, name="Universe"):
    def __init__(self, bot):
        self.universe_store = UniverseStore(bot)

        self.save_all.start()

    def cog_unload(self):
        self.save_all.cancel()

    @tasks.loop(seconds=60)
    async def save_all(self):
        """Save modified universes every minute."""

        self.universe_store.save_all()

    @save_all.after_loop
    async def save_all_final(self):
        """Save modified universes before shutting down."""

        self.universe_store.save_all()

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def new_universe(self, context):
        """
        Set up a Starflake universe in the current server.

        This will create multiple channels under a new category called
        Starflake. **If the category is deleted, you will lose access to your
        universe.** You are free to rename anything or change the channel
        descriptions, however commands only work from inside the section.
        """

        # Shown in the audit log
        reason = f"{context.author.name} asked for a new universe to be set up."

        async with context.channel.typing():
            category = await context.guild.create_category("Starflake", reason=reason)
            universe = self.universe_store.create(category.id)
            channels = await asyncio.gather(
                LoreChannel(category, universe).create(reason),
                CommandsChannel(category, universe).create(reason),
            )

        embed = discord.Embed(
            title="New universe created",
            description=f"Go to {channels[1].mention} to start playing!",
        )
        await context.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.check(with_universe)
    async def delete_universe(self, context):
        """Delete the current universe and all related channels."""

        # Shown in the audit log
        reason = (
            f"{context.author.name} asked for universe {context.universe.id_} to be deleted."
        )

        for channel in context.channel.category.text_channels:
            await channel.delete(reason=reason)
        await context.channel.category.delete(reason=reason)

        self.universe_store.delete(context.universe)


def setup(bot):
    bot.add_cog(UniverseCog(bot))
