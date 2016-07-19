from discord.ext import commands
import discord
from token_and_api_key import *
from stat_func import *
from hero_graph import hero_per_month

class Stats:
    '''Match-related stats'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def last(self, ctx, *, number: int):
        player_id = player_dic[ctx.message.author.name]
        reply = last_match(player_id, characters)  # !last 0 == last match

        await self.bot.send_file(
            ctx.message.channel, 'images/heroes/lineup/lineup.png', content=reply)
        await self.bot.send_file(
            ctx.message.channel, 'images/heroes/lineup/itemlist.png')

    @commands.command(pass_context=True)
    async def p_last(self, ctx, *, characters: str):
        player_id = player_dic[characters.split()[1]]
        number = int(characters.split()[0])
        reply = last_match(player_id, number)

        await self.bot.send_file(
            ctx.message.channel, 'images/heroes/lineup/lineup.png', content=reply)
        await self.bot.send_file(
            ctx.message.channel, 'images/heroes/lineup/itemlist.png')

    @commands.command(pass_context=True)
    async def stats(self, ctx, games: int):
        player_id = player_dic[ctx.message.author.name]
        reply = avg_stats(player_id, games)
        await self.bot.say(reply)

    @commands.command(pass_context=True)
    async def wr(self, ctx, hero_name):
        player_id = player_dic[ctx.message.author.name]
        try:
            hero_id = list(hero_dic.keys())[
                list(hero_dic.values()).index(hero_name)]
        except ValueError:
            await self.bot.say("Invalid hero name")
        reply = winrate_hero(player_id, hero_id)
        await self.bot.say(reply)


    @commands.command(pass_context=True)
    async def wr_with(self, ctx, *, msg):
        names = msg.split()
        player_id = player_dic[ctx.message.author.name]
        for i, name in enumerate(names):
            names[i] = player_dic[name]
        reply = winrate_with(player_id, names)
        await self.bot.say(reply)


    @commands.command(pass_context=True)
    async def wr_with_hero(self, ctx, *, msg):
        player_id = player_dic[ctx.message.author.name]
        player_id2 = player_dic[msg.split()[0]]
        hero_name = ' '.join(msg.split()[1:])
        hero_id = list(hero_dic.keys())[list(
            hero_dic.values()).index(hero_name)]

        reply = my_winrate_with_player_on(player_id, player_id2, hero_id)
        await self.bot.say(reply)


    @commands.command(pass_context=True)
    async def avg(self, ctx, *, hero_name):
        player_id = player_dic[ctx.message.author.name]
        hero_id = list(hero_dic.keys())[
            list(hero_dic.values()).index(hero_name)]
        reply = avg_stats_with_hero(player_id, hero_id)
        await self.bot.say(reply)


    @commands.command(pass_context=True)
    async def game_stat(self, ctx, match_number: int):
        player_id = player_dic[ctx.message.author.name]
        reply = last_match(player_id, match_number)
        big_pic(player_id, match_number)
        await self.bot.send_file(ctx.message.channel,
            'images/heroes/lineup/itemlist2.png',
            content=reply
            )

    @commands.command(pass_context=True)
    async def hero_graph(self, ctx, hero_name):
            player_id = player_dic[ctx.message.author.name]
            hero_id = list(hero_dic.keys())[
                list(hero_dic.values()).index(hero_name)]
            reply = hero_per_month(player_id, hero_id)
            await self.bot.send_file(
                    ctx.message.channel,
                    'images/graphs/hero.png',
                    content=reply)


    @commands.command(pass_context=True)
    async def records(self, ctx, *hero_name):
        player_id = player_dic[ctx.message.author.name]
        if hero_name:
            hero_id = list(hero_dic.keys())[
                list(hero_dic.values()).index(hero_name[0])]
            reply = all_time_records(player_id, hero_id)
        else:
            reply = all_time_records(player_id)
        await self.bot.say(reply)


def setup(bot):
    bot.add_cog(Stats(bot))
