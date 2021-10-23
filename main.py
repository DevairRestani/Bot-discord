import discord
from discord.ext import commands
import os

testing = False

client = commands.Bot(command_prefix = "-", case_insensitive = True)
    

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run('NzYyMzQ4NTM0MjE2MzkyNzM0.X3n2Zg.KQQMFnvnd2jzv6O_geds-yQz8Ns')