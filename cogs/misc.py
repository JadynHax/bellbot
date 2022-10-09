import discord, os
from checks import *
from discord.ext import commands


# Miscellaneous cog
class Miscellaneous(
    commands.Cog,
    name="Miscellaneous",
    command_attrs=dict(case_insensitive=True),
):
    "Miscellaneous commands."

    def __init__(self, bot):
        self.bot = bot
        self.bot.help_command.cog = self

    # Send invite link
    @commands.command(name="invite", aliases=["inv", "i"])
    async def invite(self, ctx):
        "Sends an invite link for the bot!"
        await ctx.send(
            "Invite me!\nhttps://discord.com/api/oauth2/authorize?client_id=1028339812278730773&permissions=268487680&scope=bot"
        )

    # Send bot latency
    @commands.command(name="ping", aliases=["latency", "l"])
    async def ping(self, ctx):
        "Pong!\nSee the bot's latency in ms."
        await ctx.send(embed=discord.Embed(title="Pong!", description=f"My latency is **{int(self.bot.latency*1000)} ms**.", color=0xc6b005))

    # Send bot credits and info
    @commands.command(name="credits", aliases=["c", "info"])
    async def info(self, ctx):
        "See the bot's creator and other information!"
        # Get bot code data
        lines, chars, files = 0, 0, 0

        for root, dirs, files_ in os.walk("."):
            if not any([ignorename in root for ignorename in [".git", "__pycache__"]]):
                for file in files_:
                    with open(os.path.join(root, file), "r") as infile:
                        contents = infile.read()

                    chars += len(contents)
                    lines += len(contents.split("\n"))
                    files += 1

        users = self.bot.get_all_members()
        users = set(users)

        embed = discord.Embed(title="Bell Bot Info & Credits", color=0xc6b005)
        embed.add_field(name="Stats", value=f"Connected to **{len(self.bot.guilds)}** servers as **{self.bot.user.name}#{self.bot.user.discriminator}**.\n**{len(users):,}** potential users in these servers.\n**{len(self.bot.data['prefixes']['guild'].values()):,}** custom guild prefixes set.\n**{len(self.bot.data['prefixes']['user'].values()):,}** custom user prefixes set.\nI have **{files:,}** files.\nWith **{lines:,}** lines of code.\nThere are **{chars:,}** characters in my source code.", inline=False)
        embed.add_field(name="Credits", value=f"**Bell Bot** is made by **JadynHax#5061**.")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Miscellaneous(bot))
