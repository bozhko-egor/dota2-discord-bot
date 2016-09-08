import discord
from discord.ext import commands
from token_and_api_key import token, client_id, log_chat_id
import time
import asyncio

initial_extensions = (
    'cogs.stats',
    'cogs.pro',
    'cogs.meta',
    'cogs.pics',
    'cogs.voice',
    'cogs.game'
    )
help_attrs = dict(hidden=True)
description = '''Hey! I'm a bot that provides Dota2 related utilities.'''
bot = commands.Bot(
    command_prefix='!',
    description=description,
    pm_help=False,
    help_attrs=help_attrs
    )


@bot.event
async def on_message(message):

    if message.author.bot:
        return

    await bot.process_commands(message)


@bot.event
async def on_command(command, ctx):
    bot.commands_used += 1


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    if not hasattr(bot, 'uptime'):
        bot.uptime = int(time.time())

if __name__ == '__main__':
    bot.commands_used = 0
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))
    launch_time = int(time.time())
    bot.client_id = client_id
    bot.run(token)
