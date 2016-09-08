from discord.ext import commands
import discord
from .utils.tournament_info import get_schedule
from .utils.parser import *

class PRO:
    """Everything related to pro games"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pro_games(self):
        """List of live or upcoming Dota2 pro games"""
        await self.bot.say(get_schedule())

    @commands.command(pass_context=True)
    async def streams(self, ctx, *, game_name):
        """Top 5 streams of <game> live on Twitch"""
        reply = get_top_streams(game_name)
        await self.bot.say(reply)


def setup(bot):
    bot.add_cog(PRO(bot))
