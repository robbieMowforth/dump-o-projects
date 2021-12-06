import os

import asyncio
import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import random

#Minecraft server import
from mcstatus import MinecraftServer
import discord
from discord.ext import commands
import time

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# bot responds to messages with the prefix below (no commands are needed for this bot)
client = discord.Client()
bot = commands.Bot(command_prefix='m.')

# This fucntion prints the bots name, what server its in and what members are on that server
@bot.event
async def on_ready():
    # possible old way for voice to work, unsure about this
    # discord.opus.load_opus('opus.dll')

    # guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)
    # guild = discord.utils.get(bot.guilds, name=GUILD)
    # above is alternate ways to preform below function (finds the guild that is given in the 'GUILD' varible
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

    await bot.change_presence(status=discord.Status.online, activity=discord.Game('Minecraft'))
    
#minecraft status
@bot.command(name='status', help="Gets the status of the minecraft server\n" +
                                  "Example input: 'm.status'")
async def status(ctx):
    
    mineServer = MinecraftServer.lookup("91.125.87.76:25565")
    status = mineServer.status()
    await ctx.send("The server has {0} players and replied in {1} ms".format(status.players.online, status.latency))

# start button
bot.run(TOKEN)
