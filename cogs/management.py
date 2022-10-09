import discord, json
from checks import *
from typing import Optional
from discord.ext import commands


# Management cog
class Management(commands.Cog, name="Management", command_attrs=dict(case_insensitive=True)):
    "Bot managing commands (prefix changes, etc.)."

    def __init__(self, bot):
        self.bot = bot

    # Get/set prefixes
    @commands.group(name="prefix", aliases=["pre", "p"])
    async def prefix(self, ctx):
        """Various prefix commands!
        If run without a subcommand, sends the prefixes you can use here."""

        if ctx.invoked_subcommand is None:
            prefix_results = await self.bot.get_prefixes(self.bot, ctx.message)

            await ctx.send(
                "You can use the following prefixes here: **"
                + "**, **".join(prefix_results)
                + "**."
            )

    # Get/set custom guild prefix
    @prefix.command(name="server", aliases=["s"])
    @commands.guild_only()
    async def guild_prefix(self, ctx, prefix: Optional[str]=None):
        """Sets the prefix for the server!
        (Setting the server prefix requires the "Manage Server" permission.)
        This overrides the global prefix ($) and will be permanent through any crashes/downtime.

        Setting the prefix to "none" (or any capitalization thereof) instead removes the prefix. If run without a prefix, it instead sends the current server prefix (does not require "Manage Server")."""

        if prefix is None:
            if ctx.guild.id in self.bot.data["prefixes"]["guild"].keys():
                await ctx.send(
                    "**{}** is my custom prefix for **{}**.".format(
                        self.bot.data["prefixes"]["guild"][str(ctx.guild.id)], ctx.guild.name
                    )
                )
            else:
                await ctx.send(f"**{ctx.guild.name}** does not have a custom prefix yet.")
        else:
            perms = ctx.message.channel.permissions_for(ctx.message.author)

            if perms.manage_guild:
                self._guild_prefix(ctx.guild.id, prefix)
                await ctx.send(
                    "Done! Your server's custom prefix {}.".format(
                        f"is now {prefix}" if prefix.lower() != "none" else "has been unset"
                    )
                )

            else:
                raise commands.MissingPermissions(["manage_guild"])

    # Set custom guild prefix
    def _guild_prefix(self, _id, prefix):
        if prefix.lower() == "none":
            self.bot.data["prefixes"]["guild"].pop(str(_id))

        else:
            self.bot.data["prefixes"]["guild"][str(_id)] = prefix

        bot.update_json()

    # Get/set custom user prefix
    @prefix.command(name="user", aliases=["u"])
    async def user_prefix(self, ctx, prefix: Optional[str]=None):
        """Sets your custom user prefix!
        Your custom prefix will persist across servers and will be permanent through any crashes/downtime.
        This does not override the global prefix ($) or any server prefixes. Instead, this is just a prefix you can use in addition to the global/server prefix.

        Setting the prefix to "none" (or any capitalization thereof) instead removes the prefix. If run without a prefix, it instead sends your current custom prefix."""

        if prefix is None:
            if ctx.message.author.id in self.bot.data["prefixes"]["user"].keys():
                await ctx.send(
                    "**{}** is your custom prefix.".format(
                        self.bot.data["prefixes"]["user"][str(ctx.message.author.id)]
                    )
                )

            else:
                await ctx.send("You don't have a custom prefix... yet!")

        else:
            if prefix.lower() == "none":
                self.bot.data["prefixes"]["user"].pop(str(ctx.message.author.id))

            else:
                self.bot.data["prefixes"]["user"][str(ctx.message.author.id)] = prefix

            bot.update_json()

            await ctx.send(
                "Done! Your custom prefix {}.".format(
                    f"is now {prefix}" if prefix.lower() != "none" else "has been unset"
                )
            )

    @commands.command(name="ignchans", aliases=["ignorechannels", "ignore", "ic"], hidden=True)
    @commands.has_guild_permissions(manage_channels=True)
    async def ignore_channels(self, ctx, channel: discord.TextChannel):
        pass


async def setup(bot):
    await bot.add_cog(Management(bot))
