from discord.ext import commands


def is_owner_check(message):
    return message.author.id == '80088516616269824'

def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx.message))
