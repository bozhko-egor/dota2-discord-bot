from discord.ext import commands
import discord



class RNG:
    """Utilities that provide pseudo-RNG."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def kek(self, ctx):
        """Displays a random thing you request."""
        if ctx.invoked_subcommand is None:
            await self.bot.say('Incorrect random subcommand passed.')

    @kek.command()
    async def weapon(self):

        await self.bot.say("kappa")


def setup(bot):
    bot.add_cog(RNG(bot))
