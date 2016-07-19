from discord.ext import commands
import discord
from tournament_info import get_schedule


class PRO:
    """Everything related to pro-games"""

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def pro_games(self):
        await self.bot.say(get_schedule())




def setup(bot):
    bot.add_cog(PRO(bot))
