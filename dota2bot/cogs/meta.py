from discord.ext import commands
import discord
import stat_func


class Meta:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def uptime(self):
        reply = stat_func.time_diff(self.bot.uptime)
        await self.bot.say(reply)


def setup(bot):
    bot.add_cog(Meta(bot))
