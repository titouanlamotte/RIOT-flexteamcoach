import discord
from discord.ext import commands
#from discord import Spotify

from pprint import pprint

import secrets

# -*- coding: utf-8 -*-


# Discord Bot Token
#TOKEN = ""
client = commands.Bot(command_prefix= '!', case_insensitive=True)

# Cog list
extensions = ['admin','lol','tft']

# ALIVE
@client.event
async def on_ready():
    print("Beep Beep beep, Time for a 🍻!")

# Load a specific cog
@client.command(brief=('load a cog: ' + ', '.join(extensions)), description=('load a cog: ' + ', '.join(extensions)))
async def load(ctx, extension):
    try:
        client.unload_extension(extension)
    except Exception as error:
        print('{} cannot be unloaded. [{}]'.format(extension, error))
    
    try:
        client.load_extension(extension)
        print('loaded {}'.format(extension))
    except Exception as error:
        print('{} cannot be loaded. [{}]'.format(extension, error))


# Unload a specific cog
@client.command(brief=('unload a cog: ' + ', '.join(extensions)), description=('unload a cog: ' + ', '.join(extensions)))
async def unload(ctx, extension):
    try:
        client.unload_extension(extension)
        print('unloaded {}'.format(extension))
    except Exception as error:
        print('{} cannot be unloaded. [{}]'.format(extension, error))



if __name__ == "__main__":
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))


client.run(secrets.TOKEN)