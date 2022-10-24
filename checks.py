import datetime
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


# Custom per-user cooldown check
def user_cooldown(cooldown: int):
    cooldown = datetime.timedelta(seconds=cooldown)
    cooldowns = {}

    def predicate(ctx):
        if (cooldown_end := cooldowns.get(ctx.author.id)) is None or cooldown_end < datetime.datetime.now():
            if ctx.valid and ctx.invoked_with in (*ctx.command.aliases, ctx.command.name):
                cooldowns[ctx.author.id] = datetime.datetime.now() + cooldown

            return True

        elif cooldowns.get(ctx.author.id) is None:
            pass

        else:
            def strfdelta(tdelta, fmt):
                d = {"d": tdelta.days}
                d["h"], rem = divmod(tdelta.seconds, 3600)
                d["m"], d["s"] = divmod(rem, 60)
                return fmt.format(**d)

            time_remaining = strfdelta(cooldowns[ctx.author.id] - datetime.datetime.now(), "{h:0>2}:{m:0>2}:{s:0>2}")

            raise commands.CheckFailure(
                f"This command is on cooldown for {time_remaining}!"
            )

    return commands.check(predicate)
