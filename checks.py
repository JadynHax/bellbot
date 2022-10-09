from discord.ext import commands


# Check if user is bot owner
def is_bot_owner():
    def predicate(ctx):
        if ctx.message.author.id == 710209345832353852:
            return True

        else:
            raise commands.CheckFailure(
                f"You aren't allowed to use this command, {ctx.author.mention}! This is only for the bot owner!"
            )

    return commands.check(predicate)


# Check if user is Tom Nook or owner
def is_tom_nook():
    def predicate(ctx):
        if ctx.message.author.id in [792601986872639520, 710209345832353852]:
            return True

        else:
            raise commands.CheckFailure(
                f"You aren't allowed to use this command, {ctx.author.mention}! This is only for Tom Nook!"
            )

    return commands.check(predicate)


# Check if user is militia or owner
def is_militia():
    def predicate(ctx):
        if str(ctx.message.author.id) in ctx.bot.data["users"].keys():
            if ctx.bot.data["users"][str(ctx.message.author.id)]["militia"]:
                return True

        raise commands.CheckFailure(
            f"You aren't allowed to use this command, {ctx.author.mention}! This is only for the Bell Militia!"
        )

    return commands.check(predicate)
