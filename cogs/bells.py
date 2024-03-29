import discord, json, time, random
from checks import *
from typing import *
from discord.ext import commands


# Bells cog
class Bells(commands.Cog, name="Bells", command_attrs=dict(case_insensitive=True)):
    "Controls the earning of bells."

    upgrade_costs = [
        98_000,
        198_000,
        348_000,
        548_000,
        758_000,
        1_248_000,
        2_498_000,
    ]

    def __init__(self, bot):
        self.bot = bot

    # Check bells
    @commands.command(name="bells", aliases=["b"])
    async def bells(self, ctx, user: Optional[Union[discord.Member, discord.User]]):
        "Check your (or someone else's) bells."
        user = user if user is not None else ctx.author

        if str(user.id) not in self.bot.data["users"].keys():
            self.bot.initiate_user(str(user.id), 0)

        if self.bot.data["users"][str(user.id)]["bells"] <= 0:
            await ctx.send("{} have any bells!".format("You don't" if user.id == ctx.author.id else "{} doesn't".format(user.display_name)))

        else:
            await ctx.send(f"{'You have' if user.id == ctx.author.id else '{} has'.format(user.display_name)} **{self.bot.data['users'][str(user.id)]['bells']:,}** bells!")

    # Check bells
    @commands.command(name="paid")
    async def paid(self, ctx, user: Optional[Union[discord.Member, discord.User]]):
        "Check how much you (or someone else) has paid to the Bell Militia."
        user = user if user is not None else ctx.author

        if str(user.id) not in self.bot.data["users"].keys():
            self.bot.initiate_user(str(user.id), 0)

        if self.bot.data["users"][str(user.id)]["paid"] <= 0:
            await ctx.send("You haven't paid any debt off!")

        else:
            await ctx.send(f"{'You have' if user.id == ctx.author.id else '{} has'.format(user.display_name)} paid **{self.bot.data['users'][str(user.id)]['paid']:,}** bells to Tom Nook!")

    # Check debt
    @commands.command(name="debt", aliases=["d"])
    async def debt(self, ctx, user: Optional[Union[discord.Member, discord.User]]):
        "Check your (or someone else's) debt."
        user = user if user is not None else ctx.author

        if str(user.id) not in self.bot.data["users"].keys():
            self.bot.initiate_user(str(user.id), 0)

        elif self.bot.data["users"][str(user.id)]["debt"] <= 0:
            await ctx.send("{} have any debt!".format("You don't" if user.id == ctx.author.id else f"{user.display_name if user.id != 792601986872639520 else 'Tom Nook'} doesn't"))

        else:
            await ctx.send(f"{'You have' if user.id == ctx.author.id else '{} has'.format(user.display_name)} **{self.bot.data['users'][str(user.id)]['debt']:,}** bells of debt!")

    # Pay user
    @commands.command(name="pay")
    async def pay(self, ctx, user: Union[discord.Member, discord.User, str], amount: int):
        "Allows you to pay someone else bells!"
        if isinstance(user, str):
            if user.lower() == "debt":
                user = self.bot.get_user(792601986872639520)

            else:
                raise ValueError(f"{user} is an invalid argument!")

        if amount > 0:
            if str(ctx.author.id) not in self.bot.data["users"]:
                self.bot.initiate_user(str(ctx.author.id), 0)

            if self.bot.data["users"][str(ctx.author.id)]["bells"] >= amount:
                if str(user.id) not in self.bot.data["users"]:
                    self.bot.initiate_user(str(user.id), 0)

                self.bot.data["users"][str(user.id)]["bells"] += amount

                if user.id == 792601986872639520:
                    if self.bot.data["users"][str(ctx.author.id)]["debt"] > 0:
                        self.bot.data["users"][str(ctx.author.id)]["debt"] -= min(amount, self.bot.data["users"][str(ctx.author.id)]["debt"])
                        self.bot.data["users"][str(ctx.author.id)]["paid"] += min(amount, self.bot.data["users"][str(ctx.author.id)]["debt"])

                elif self.bot.data["users"][str(user.id)]["militia"]:
                    if self.bot.data["users"][str(ctx.author.id)]["debt"] > 0:
                        self.bot.data["users"][str(ctx.author.id)]["debt"] -= min(amount, self.bot.data["users"][str(ctx.author.id)]["debt"])
                        self.bot.data["users"][str(user.id)]["debt"] += min(amount, self.bot.data["users"][str(ctx.author.id)]["debt"])
                        self.bot.data["users"][str(ctx.author.id)]["paid"] += min(amount, self.bot.data["users"][str(ctx.author.id)]["debt"])
                        self.bot.data["users"][str(user.id)]["paid"] -= min(amount, self.bot.data["users"][str(ctx.author.id)]["debt"])

                self.bot.data["users"][str(ctx.author.id)]["bells"] -= amount
                self.bot.update_json()

                await ctx.send(f"Successfully paid {user.display_name if user.id != 792601986872639520 else 'Tom Nook'} **{amount:,}** bells!")

            else:
                await ctx.send("You don't have enough bells!")

        else:
            await ctx.send("Invalid amount of bells to send!")

    @commands.command(name="work")
    @user_cooldown(17_280)
    async def work(self, ctx):
        "Work to earn more bells!\nYou can do this up to 5 times per day (about every 5 hours)."
        if str(ctx.author.id) not in self.bot.data["users"].keys():
            self.bot.initiate_user(str(ctx.author.id), 0)

        gained = random.randrange(100, 251)
        activity = random.choice(["growing crops", "catching bugs", "digging for fossils", "trading turnips on the stalk market", "fishing", "shooting down balloons"])

        self.bot.data["users"][str(ctx.author.id)]["bells"] += gained
        self.bot.update_json()

        await ctx.send(f"You earned **{gained}** bells from {activity}!")

    @commands.command(name="upgrade-house", aliases=["upgrade", "uh"])
    async def upgrade_house(self, ctx):
        "Upgrade your house! (Gives you more debt but you can brag now)"
        if str(ctx.author.id) not in self.bot.data["users"].keys():
            self.bot.initiate_user(str(ctx.author.id), 0)

        if self.bot.data["users"][str(ctx.author.id)]["debt"] <= 0 and self.bot.data["users"][str(ctx.author.id)]["house"] < 7:
            self.bot.data["users"][str(ctx.author.id)]["debt"] += self.upgrade_costs[self.bot.data["users"][str(ctx.author.id)]["house"]]
            self.bot.data["users"][str(ctx.author.id)]["house"] += 1

            self.bot.update_json()

            await ctx.send(f"Your house has been upgraded to level **{self.bot.data['users'][str(ctx.author.id)]['house']}**, leaving you **{self.bot.data['users'][str(ctx.author.id)]['debt']:,}** bells in debt!")

        elif self.bot.data["users"][str(ctx.author.id)]["house"] == 7:
            await ctx.send("Your house is already maximum level (7)!")

        else:
            await ctx.send(f"You have **{self.bot.data['users'][str(ctx.author.id)]['debt']:,}** bells of debt, so you can't upgrade yet!")

    @commands.command(name="house", aliases=["h"])
    async def house(self, ctx, user: Optional[Union[discord.Member, discord.User]]):
        "Show off your house!"
        user = user if user is not None else ctx.author

        if str(user.id) not in self.bot.data["users"].keys():
            self.bot.initiate_user(str(user.id), 0)

        await ctx.send("{} house is level **{}**!".format("Your" if user.id == ctx.author.id else "{}'s".format(user.display_name), self.bot.data["users"][str(user.id)]["house"]))

async def setup(bot):
    await bot.add_cog(Bells(bot))
