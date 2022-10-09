import discord
from checks import *
from typing import *
from discord.ext import commands


# Militia cog
class Militia(commands.Cog, name="Militia", command_attrs=dict(case_insensitive=True, hidden=True)):
    "Commands related to the Bell Militia"

    def __init__(self, bot):
        self.bot = bot


    # Add debt
    @commands.command(name="add-debt", aliases=["ad"])
    @is_tom_nook()
    async def add_debt(self, ctx, user: Union[discord.Member, discord.User], amount: int):
        "Adds to a user's debt (Tom Nook only)."
        if str(user.id) not in self.bot.data["users"]:
            self.bot.initiate_user(str(user.id), 0)

        self.bot.data["users"][str(user.id)]["debt"] += amount

        self.bot.update_json()

        await ctx.send(f"Successfully altered {user.display_name}'s debt!\nTheir debt is now {self.bot.data['users'][str(user.id)]['debt']:,} bells!")


    # Add debt to everyone in the system
    @commands.command(name="all-debt")
    @is_tom_nook()
    async def all_debt(self, ctx, amount: int):
        "Increase everyone's debt by an amount"
        for user in self.bot.data["users"].keys():
            if user != "792601986872639520":
                self.bot.data["users"][user]["debt"] += amount

        self.bot.update_json()

        await ctx.send(f"Increased everyone's debt by {amount:,} bells!")


    # Make a user a militia member
    @commands.command(name="make-militia", aliases=["mm"])
    @is_tom_nook()
    async def make_militia(self, ctx, user: Union[discord.Member, discord.User]):
        "Makes a user a member of the Bell Militia."
        if str(user.id) not in self.bot.data["users"]:
            self.bot.initiate_user(str(user.id), 0)

        if not self.bot.data["users"][str(user.id)]["militia"]:
            self.bot.data["users"][str(user.id)]["militia"] = True

            self.bot.update_json()

            await ctx.send(f"Successfully made {user.display_name} a member of the Bell Militia!")

        else:
            await ctx.send(f"{user.display_name} is already a member of the Bell Militia!")


    # Revoke a user's militia status
    @commands.command(name="revoke-militia", aliases=["remove-militia", "rm"])
    @is_tom_nook()
    async def revoke_militia(self, ctx, user: Union[discord.Member, discord.User]):
        "Revokes a user's Bell Militia status."
        if str(user.id) not in self.bot.data["users"]:
            self.bot.initiate_user(str(user.id), 0)

        if self.bot.data["users"][str(user.id)]["militia"]:
            self.bot.data["users"][str(user.id)]["militia"] = False

            self.bot.update_json()

            await ctx.send(f"Successfully revoked {user.display_name}'s Bell Militia membership!")

        else:
            await ctx.send(f"{user.display_name} is not a member of the Bell Militia!")


    # Allow militia members to take bells
    @commands.command(name="take-bells")
    @is_militia()
    @commands.cooldown(1, 86_400.0, commands.BucketType.user)
    async def take_bells(self, ctx, user: Union[discord.Member, discord.User], amount: int):
        "Allows Bell Militia to take someone's bells (up to 2,500) once per day."
        if str(user.id) not in self.bot.data["users"]:
            self.bot.initiate_user(str(user.id), 0)

        if 0 < amount <= 2_500 and not self.bot.data["users"][str(user.id)]["militia"]:
            if self.bot.data["users"][str(user.id)]["bells"] >= amount:
                self.bot.data["users"][str(ctx.author.id)]["bells"] += amount
                self.bot.data["users"][str(user.id)]["bells"] -= amount

                if self.bot.data["users"][str(user.id)]["debt"] > 0:
                    self.bot.data["users"][str(user.id)]["debt"] -= min(amount, self.bot.data["users"][str(user.id)]["debt"])
                    self.bot.data["users"][str(user.id)]["paid"] += min(amount, self.bot.data["users"][str(user.id)]["debt"])
                    self.bot.data["users"][str(ctx.author.id)]["debt"] += min(amount, self.bot.data["users"][str(ctx.author.id)]["debt"])
                    self.bot.data["users"][str(ctx.author.id)]["paid"] -= min(amount, self.bot.data["users"][str(ctx.author.id)]["debt"])

                self.bot.update_json()

                await ctx.send(f"Successfully took {amount:,} bells from {user.display_name}!")

            else:
                await ctx.send(f"{user.display_name} doesn't have enough bells!")

        elif self.bot.data["users"][str(user.id)]["militia"]:
            await ctx.send("Cannot take bells from militia!")
            take_bells.reset_cooldown(ctx)

        else:
            await ctx.send("Invalid amount of bells to take!")
            take_bells.reset_cooldown(ctx)



async def setup(bot):
    await bot.add_cog(Militia(bot))
