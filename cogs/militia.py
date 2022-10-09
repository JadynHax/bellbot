import discord
from checks import *
from discord.ext import commands


# Militia cog
class Militia(commands.Cog, name="Militia", command_attrs=dict(case_insensitive=True, hidden=True)):
    "Commands related to the Bell Militia"

    def __init__(self, bot):
        self.bot = bot


    # Add debt
    @commands.command(name="add-debt", aliases=["ad"])
    @is_tom_nook()
    async def add_debt(self, ctx, user: discord.User, amount: int):
        "Adds to a user's debt (Tom Nook only)."
        if str(user.id) not in self.bot.data["users"]:
            self.bot.initiate_user(str(user.id), 0)

        self.bot.data["users"][str(user.id)]["debt"] += amount

        self.bot.update_json()

        await ctx.send(f"Successfully altered {user.display_name}'s debt!\nTheir debt is now {self.bot.data['users'][str(user.id)]['debt']:,} bells!")


    # Make a user a militia member
    @commands.command(name="make-militia", aliases=["mm"])
    @is_tom_nook()
    async def make_militia(self, ctx, user: discord.User):
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
    async def revoke_militia(self, ctx, user: discord.User):
        "Revokes a user's Bell Militia status."
        if str(user.id) not in self.bot.data["users"]:
            self.bot.initiate_user(str(user.id), 0)

        if self.bot.data["users"][str(user.id)]["militia"]:
            self.bot.data["users"][str(user.id)]["militia"] = False

            self.bot.update_json()

            await ctx.send(f"Successfully revoked {user.display_name}'s Bell Militia membership!")

        else:
            await ctx.send(f"{user.display_name} is not a member of the Bell Militia!")


async def setup(bot):
    await bot.add_cog(Militia(bot))
