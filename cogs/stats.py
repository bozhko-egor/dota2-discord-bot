from discord.ext import commands
import discord
from token_and_api_key import *
from .utils import stat_func as sf
from .utils.hero_graph import hero_per_month
from .utils.hero_dictionary import hero_dic
from .utils.resources import db
from csv import reader


class Stats:
    """Dota-related stats"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def last(self, ctx, *, number: int):
        """!last 0 - your last match"""
        player_id = db.get_acc_id(ctx.message.author.id, ctx.message.server.id)
        reply = sf.last_match(player_id, number)  # !last 0 == last match

        await self.bot.send_file(
            ctx.message.channel, 'images/lineup/lineup.png', content=reply)
        await self.bot.send_file(
            ctx.message.channel, 'images/lineup/itemlist.png')

    @commands.command(pass_context=True)
    async def p_last(self, ctx, number: int, *, player_name: str):
        """Same as !last but for another player"""
        members = ctx.message.server.members
        discord_id = 0
        for member in members:
            if player_name == member.name:
                discord_id = member.id
        if discord_id:

            reply = sf.last_match(
                db.get_acc_id(discord_id, ctx.message.server.id),
                number)

            await self.bot.send_file(
                ctx.message.channel, 'images/lineup/lineup.png', content=reply)
            await self.bot.send_file(
                ctx.message.channel, 'images/lineup/itemlist.png')
        else:
            await self.bot.say('Invalid player name')


    @commands.command(pass_context=True)
    async def stats(self, ctx, games: int):
        """Your average stats in last <n> games"""
        player_id = db.get_acc_id(ctx.message.author.id, ctx.message.server.id)
        reply = sf.avg_stats(player_id, games)
        await self.bot.say(reply)

    @commands.command(pass_context=True)
    async def wr(self, ctx, hero_name):
        """Your winrate playing as a <hero_name>"""
        player_id = db.get_acc_id(ctx.message.author.id, ctx.message.server.id)
        try:
            hero_id = list(hero_dic.keys())[
                list(hero_dic.values()).index(hero_name)]
        except ValueError:
            await self.bot.say("Invalid hero name")
        reply = sf.winrate_hero(player_id, hero_id)
        await self.bot.say(reply)

    @commands.command(pass_context=True)
    async def wr_with(self, ctx, *, msg):
        """Your winrate with players (takes up to 4 arguments)"""
        names = msg.split()
        player_id = db.get_acc_id(ctx.message.author.id, ctx.message.server.id)
        players = []
        for member in ctx.message.server.members:
            for name in names:
                if name == member.name:
                    players.append(db.get_acc_id(
                        member.id,
                        ctx.message.server.id
                        )
                        )
        reply = sf.winrate_with(player_id, players)
        await self.bot.say(reply)

    @commands.command(pass_context=True)
    async def wr_with_hero(self, ctx, player_name, *, hero_name):
        """Your winrate with <player> on specific <hero>"""
        player_id = db.get_acc_id(ctx.message.author.id, ctx.message.server.id)
        discord_id = 0
        for member in ctx.message.server.members:
            if player_name == member.name:
                discord_id = member.id
        if discord_id:
            player_id2 = db.get_acc_id(discord_id, ctx.message.server.id)
            hero_id = list(hero_dic.keys())[list(
                hero_dic.values()).index(hero_name)]

            reply = sf.my_winrate_with_player_on(player_id, player_id2, hero_id)
            await self.bot.say(reply)
        else:
            await self.bot.say('Invalid player name')

    @commands.command(pass_context=True)
    async def avg(self, ctx, *, hero_name):
        """Your average stats playing as a <hero_name>"""
        player_id = db.get_acc_id(ctx.message.author.id, ctx.message.server.id)
        hero_id = list(hero_dic.keys())[
            list(hero_dic.values()).index(hero_name)]
        reply = sf.avg_stats_with_hero(player_id, hero_id)
        await self.bot.say(reply)

    @commands.command(pass_context=True)
    async def game_stat(self, ctx, match_number: int):
        """End-game screen with kda and items for all players. !game_stat 0 - your last match"""
        player_id = db.get_acc_id(ctx.message.author.id, ctx.message.server.id)
        reply = sf.last_match(player_id, match_number)
        sf.big_pic(player_id, match_number)
        await self.bot.send_file(
            ctx.message.channel,
            'images/lineup/itemlist2.png',
            content=reply
            )

    @commands.command(pass_context=True)
    async def hero_graph(self, ctx, hero_name):
        """Graph with your number of games played as a <hero_name> per month"""
        player_id = db.get_acc_id(ctx.message.author.id, ctx.message.server.id)
        hero_id = list(hero_dic.keys())[
            list(hero_dic.values()).index(hero_name)]
        reply = hero_per_month(player_id, hero_id)
        await self.bot.send_file(
                ctx.message.channel,
                'images/graphs/hero.png',
                content=reply)

    @commands.command(pass_context=True)
    async def records(self, ctx, *hero_name):
        """Your all-time records. Also takes <hero_name> argument for records as a hero"""
        player_id = db.get_acc_id(ctx.message.author.id, ctx.message.server.id)
        if hero_name:
            hero_id = list(hero_dic.keys())[
                list(hero_dic.values()).index(hero_name[0])]
            reply = sf.all_time_records(player_id, hero_id)
        else:
            reply = sf.all_time_records(player_id)
        await self.bot.say(reply)


def setup(bot):
    bot.add_cog(Stats(bot))
