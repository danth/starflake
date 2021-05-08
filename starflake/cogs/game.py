import discord
import jsons
from discord.ext import commands, tasks

from starflake.game_objects.game import GameStore, with_game


class GameCog(commands.Cog, name="Game"):
    def __init__(self, bot):
        self.game_store = GameStore(bot)

        self.save_all.start()

    def cog_unload(self):
        self.save_all.cancel()

    @tasks.loop(seconds=60)
    async def save_all(self):
        """Save modified games every minute."""

        self.game_store.save_all()

    @save_all.after_loop
    async def save_all_final(self):
        """Save modified games before shutting down."""

        self.game_store.save_all()

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def new_game(self, context):
        """Set up a Starflake game in the current server."""

        # Shown in the audit log
        reason = f"{context.author.name} asked for a new game to be set up."

        category = await context.guild.create_category("Starflake", reason=reason)
        channel = await context.guild.create_text_channel(
            "starflake", category=category, reason=reason
        )

        self.game_store.create(category.id)

        embed = discord.Embed(
            title="New game created",
            description=f"Go to {channel.mention} to start playing!",
        )
        await context.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.check(with_game)
    async def delete_game(self, context):
        """Delete the current game and all related channels."""

        # Shown in the audit log
        reason = f"{context.author.name} asked for game {context.game.id_} to be deleted."

        for channel in context.channel.category.text_channels:
            await channel.delete(reason=reason)
        await context.channel.category.delete(reason=reason)

        self.game_store.delete(context.game)


def setup(bot):
    bot.add_cog(GameCog(bot))
