from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.utils import find, get
from tinydb import TinyDB, where
import discord, asyncio, time, json

# checks prefix database for each message. could probably improve this
default_prefix = "."

def prefix(bot, message):
    prefixList = TinyDB('databases/prefixdb.json')
    results = prefixList.search(where('id') == message.guild.id)
    if results:
        prefix = results[0]['prefix']
    else:
        prefix = default_prefix
    return prefix

intents = discord.Intents.default()
intents.members = True 
bot = commands.Bot(command_prefix=prefix, case_insensitive=True,intents=intents)

# read config information
with open("config.json") as file:
    config_json = json.load(file)
    TOKEN = config_json["token"]

#################
#   Bot Stuff   #
#################
@bot.event
async def on_ready():
    print(discord.__version__)
    print("Connected..")
    CurrentGuildCount = 0
    for _ in bot.guilds:
        CurrentGuildCount += 1

    print('Current Server Count: ' + str(CurrentGuildCount))
    await bot.change_presence(activity=discord.Game(name='.help | discord.gg/49UEBnH'))

@bot.event
async def on_message(message):
    ctx = await bot.get_context(message)
    await bot.invoke(ctx)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

@bot.event
async def on_guild_join(guild):
    c = bot.get_channel(766744455079788654)
    message = f'```Joined Server: {guild.name}\nOwner: {guild.owner.name}#{guild.owner.discriminator}\nMember Count: {str(guild.member_count)}\nDate Made: {str(guild.created_at)}```'
    await c.send(message)
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send("Thanks for inviting me! You can get started by typing .help to find the current command list and change the command prefix by typing .setprefix followed by the desired prefix e.g. !.\nSource Code: https://github.com/Amexy/sekai-bot\nSupport: https://ko-fi.com/lisabot\nIf you have any feedback or requests, please dm Josh#1373 or join discord.gg/49UEBnH.")


bot.remove_command('help')
bot.load_extension('commands.cogs.event')
bot.load_extension("commands.cogs.help")
bot.load_extension("commands.cogs.misc")
bot.load_extension("commands.cogs.moderation")
bot.load_extension("commands.cogs.loops")
bot.load_extension("commands.cogs.updates")

bot.run(TOKEN)
