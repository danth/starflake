import discord

from starflake.channels import Channel


class CommandsChannel(Channel):
    """A channel used for bot commands."""

    name = "commands"
    topic = "Interact with Starflake here. Send +help for a list of available commands."

    @property
    def overwrites(self):
        return {
            self.category.guild.default_role: discord.PermissionOverwrite(
                # Disabling history means users will only see new messages
                # while they are focused on the channel.
                read_message_history=False
            ),
        }
