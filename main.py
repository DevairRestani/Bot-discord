from discord.ext import commands
import os
import time

from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')


client = commands.Bot(command_prefix = "-", case_insensitive = True)
    

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
  

client.run(TOKEN)

print("Bot ok...")