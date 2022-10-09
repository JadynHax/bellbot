import discord, os, json
from checks import *
from discord.ext import commands


# Owner cog
class Owner(commands.Cog, name="Owner", command_attrs=dict(case_insensitive=True, hidden=True)):
    "Owner commands."

    def __init__(self, bot):
        self.bot = bot


    # Add cog reload command for hotfixes
    @commands.command(name="reload")
    @is_bot_owner()
    async def reload(self, ctx, ext: str):
        msg = await ctx.send(f"Reloading extension `{ext}`...")

        try:
            await self.bot.reload_extension(ext)
            await msg.edit(content=f"`{ext}` reloaded!")
            print(f"Extension reloaded: {ext}")

        except Exception as e:
            await msg.edit(content=f"Error reloading `{ext}`!\n```{e}```")


    # Add cog load command for hotfixes
    @commands.command(name="load")
    @is_bot_owner()
    async def load(self, ctx, ext: str):
        msg = await ctx.send(f"Loading extension `{ext}`...")

        try:
            await self.bot.load_extension(ext)
            await msg.edit(content=f"`{ext}` loaded!")
            print(f"Extension loaded: {ext}")

        except Exception as e:
            await msg.edit(content=f"Error loading `{ext}`!\n```{e}```")


    # Add cog unload command for hotfixes
    @commands.command(name="unload")
    @is_bot_owner()
    async def unload(self, ctx, ext: str):
        msg = await ctx.send(f"Unloading extension `{ext}`...")

        try:
            await self.bot.unload_extension(ext)
            await msg.edit(content=f"`{ext}` unloaded!")
            print(f"Extension unloaded: {ext}")

        except Exception as e:
            await msg.edit(content=f"Error unloading `{ext}`!\n```{e}```")


    # Add bot data load command
    @commands.command(name="load-data")
    @is_bot_owner()
    async def load_data(self, ctx):
        msg = await ctx.send("Loading bot data...")

        try:
            with open(os.path.join(".", "bot-data.json"), "r") as datafile:
                bot_data = json.load(datafile)

            await msg.edit(content="Bot data loaded!")
            print("Bot data loaded")

        except Exception as e:
            await msg.edit(content=f"Error loading bot data!\n```{e}```")


async def setup(bot):
    await bot.add_cog(Owner(bot))
