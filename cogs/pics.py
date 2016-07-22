from discord.ext import commands
import discord
from .utils.hero_dictionary import hero_dic, item_dic

class Pics:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def hero(self, ctx, *, hero_name):
        """<hero_name>'s icon"""
        if hero_name.lower() in [x.lower() for x in hero_dic.values()]:
            await self.bot.send_file(
                ctx.message.channel,
                'images/heroes/{} icon.png'.format(hero_name.lower())
                )

        else:
            await self.bot.say('Invalid hero name')

    @commands.command(pass_context=True)
    async def item(self, ctx, *, item_name):
        """Picture of <item_name>"""
        if item_name.lower() in [x.lower() for x in item_dic.values()]:
            await self.bot.send_file(
                ctx.message.channel,
                'images/items/{} icon.png'.format(item_name.lower())
                )

        else:
            await self.bot.say('Invalid item name')

    @commands.command(pass_context=True)
    async def wow(self, ctx):
        """Eddy Wally"""
        await self.bot.send_file(
            ctx.message.channel,
            'images/wow.png'
            )

def setup(bot):
    bot.add_cog(Pics(bot))
