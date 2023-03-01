import discord, asyncio, json, os, sys, random, time
import textwrap as tw
from exceptions import *
from checks import *
from discord.ext import commands


# Ensure bot data exists
if not os.path.exists(os.path.join(".", "bot-data.json")):
    print("Bot data not found! Generating bot data file...", file=sys.stderr)

    with open(os.path.join(".", "bot-data.json"), "w") as datafile:
        json.dump({
            "token": input("Input bot token:\n> "),
            "prefixes": {
                "global": [input("Input bot global prefix:\n> ")],
                "guild": {},
                "user": {}
            },
            "users": {},
        }, datafile)

# Load bot data
with open(os.path.join(".", "bot-data.json"), "r") as datafile:
    bot_data = json.load(datafile)

# Ensure proper data format
if not isinstance(bot_data, dict):
    raise InvalidDataException("Bot data is invalid!")


# Gets possible prefixes to use
async def get_prefixes(bot, message):
    guild = message.guild
    prefix_results = []
    if guild:
        if str(guild.id) in bot.data["prefixes"]["guild"].keys():
            prefix_results.append(bot.data["prefixes"]["guild"][str(guild.id)])

        else:
            for item in bot.data["prefixes"]["global"]:
                prefix_results.append(item)

    else:
        for item in bot.data["prefixes"]["global"]:
            prefix_results.append(item)

    if str(message.author.id) in bot.data["prefixes"]["user"].keys():
        prefix_results.append(bot.data["prefixes"]["user"][str(message.author.id)])

    return commands.when_mentioned_or(*prefix_results)(bot, message)


# Update json function
def update_json():
    with open(os.path.join(".", "bot-data.json"), "w") as datafile:
        json.dump(bot.data, datafile)


# Initiate user function
def initiate_user(user_id, bells):
        bot.data["users"][user_id] = {
            "bells": bells,
            "paid": 0,
            "debt": 49_800,
            "militia": False,
            "house": 0,
        }

        bot.update_json()


# Initiate bot with members and message_content intents set to True
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=get_prefixes, intents=intents, case_insensitive=True)

# Managing command errors
@bot.event
async def on_command_error(ctx, exception):
    if isinstance(exception, (commands.CheckFailure, commands.CheckAnyFailure, commands.MissingPermissions)):
        await ctx.send(exception)

    elif isinstance(exception, commands.CommandNotFound):
        message = await ctx.send(exception)
        await asyncio.sleep(5)
        await message.delete()
    else:
        await ctx.send(f"```\n{exception}\n```")
        print(exception)


# Add on message processing
@bot.event
async def on_message(message):
    if not any([message.content.strip("$").startswith(char) for char in "0123456789"]):
        await bot.process_commands(message)

    if message.author.id != bot.user.id:
        if (message.author.id not in bot.cooldowns.keys()) or (bot.cooldowns[message.author.id] < time.time()):
            if str(message.author.id) in bot.data["users"].keys():
                bot.data["users"][str(message.author.id)]["bells"] += random.randrange(25, 51)

            else:
                bot.initiate_user(str(message.author.id), random.randrange(25, 51))

            bot.update_json()
            bot.cooldowns[message.author.id] = time.time() + 60.0


# Run some important functions on ready
@bot.event
async def on_ready():
    # Get bot code data
    lines, chars, files = 0, 0, 0
    largest_file = {
        "path": "filename",
        "chars": 0,
    }

    for root, dirs, files_ in os.walk("."):
        if not any([ignorename in root for ignorename in [".git", "__pycache__"]]):
            for file in files_:
                with open(os.path.join(root, file), "r") as infile:
                    contents = infile.read()

                if len(contents) > largest_file["chars"]:
                    largest_file["path"] = os.path.join(root, file)
                    largest_file["chars"] = len(contents)

                chars += len(contents)
                lines += len(contents.split("\n"))
                files += 1

    users = bot.get_all_members()
    users = set(users)

    # Display data
    print(
        tw.dedent(
            f"""\
            +------------------------------------------------------------------------------+
            | Bell Bot Stats & Info                                                        |
            |     User info:                                                               |
            |         ID:             {bot.user.id   :<20}                                 |
            |         Username:       {bot.user.name[:24]:<24}                             |
            |         Discriminator:  #{bot.user.discriminator:<28}                        |
            |     # Guilds:           {len(bot.guilds):<22,}                               |
            |     # Users:            {len(users):<17,}                                    |
            |     Prefixes:                                                                |
            |         Global:         {"  ".join(bot_data["prefixes"]["global"]):<47}      |
            |         # Guild:        {len(bot_data["prefixes"]["guild"]):<41,}            |
            |         # User:         {len(bot_data["prefixes"]["user"]):<40,}             |
            +------------------------------------------------------------------------------+
            | Code Stats                                                                   |
            |     Files:              {files:<12,}                                         |
            |     Lines:              {lines:<12,}                                         |
            |     Characters:         {chars:<12,}                                         |
            |     Largest file:                                                            |
            |         Path:           {largest_file["path"][:50]:<50}   |
            |         Characters:     {largest_file["chars"]:<28,}                         |
            +------------------------------------------------------------------------------+
            | Licensing Information                                                        |
            |     License:          MIT License. See LICENSE for details.                  |
            |     Copyright:        Copyright (c) 2022-2023 Jadyn Rutz (JadynHax)          |
            +------------------------------------------------------------------------------+
            """
        ).strip("\n")
    )

    # Load bot cogs
    with os.scandir(".\cogs") as dir:
        for entry in dir:
            if entry.is_file():
                await bot.load_extension(f"cogs.{os.path.splitext(entry.name)[0]}")
                print(f"Extension loaded: cogs.{os.path.splitext(entry.name)[0]}")

    # Change bot presence
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("with your bells"))

    # Add shutdown commmand
    @bot.command(name="shutdown", aliases=["fuckoff", "begone", "gtfo", "bye", "killbot"], hidden=True, case_insensitive=True)
    @is_bot_owner()
    async def shutdown(ctx):
        print("Shutdown command run!")
        await ctx.send("Disconnecting...")
        await bot.change_presence(status=discord.Status.offline)
        await bot.close()
        os.kill(os.getpid(), 9)


# Attach usable info to bot instance
bot.data = bot_data
bot.get_prefixes = get_prefixes
bot.update_json = update_json
bot.initiate_user = initiate_user
bot.cooldowns = {}

# Run the bot
bot.run(bot_data["token"])
