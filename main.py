import asyncio
import discord
from discord.ext import commands
from TOKEN import TOKEN
import os
import sqlite3


client = commands.Bot(command_prefix='$', intents=discord.Intents.all(), help_command=None)
client.remove_command('help')
con = sqlite3.connect('bot.db')
cur = con.cursor()


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await client.load_extension(f'cogs.{filename[:-3]}')
                print(f'{filename[:-3]} loaded')
            except Exception as e:
                print(e)


async def main():
    async with client:
        await load_extensions()
        await client.start(TOKEN)


asyncio.run(main())

