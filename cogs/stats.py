from discord.ext import commands
import discord
from .utils import stats_related as sf
from .utils.hero_graph import hero_per_month
from .utils.hero_dictionary import hero_dic
from .utils.resources import db
from csv import reader
from .utils.post_game_screen import post_game
import shlex
from opendota_api.matches import Match
from opendota_api.player import Player
import datetime
from tabulate import tabulate
import collections


class Stats:
    """Dota-related stats"""
    def __init__(self, bot):
        self.bot = bot

    def winrate(self, dic):
        matches = dic['win'] + dic['lose']
        return round(dic['win'] * 100 / (matches), 2), matches

    @commands.group(pass_context=True)
    async def last(self, ctx):
        """!last - your last match"""
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid sub command passed')

    @last.command(pass_context=True)
    async def brief(self, ctx):
        player_id = db.get_acc_id(ctx.message.author.id, ctx.message.server.id)
        reply = sf.last_match(player_id, 0, ctx)

        await self.bot.send_file(
            ctx.message.channel, 'images/lineup/lineup.png', content=reply)
        await self.bot.send_file(
            ctx.message.channel, 'images/lineup/itemlist.png')

    @last.command(pass_context=True)
    async def full(self, ctx):
        player_id = db.get_acc_id(ctx.message.author.id, ctx.message.server.id)
        match_id = Player(player_id).stat_func('matches')[0]['match_id']
        post_game(match_id)
        await self.bot.send_file(ctx.message.channel, 'images/lineup/postgame.png')

    @commands.group(pass_context=True)
    async def p_last(self, ctx):
        """Same as !last but for another player"""
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid sub command passed')

    @p_last.command(pass_context=True, name='brief')
    async def _brief(self, ctx, *, player_name):
        members = ctx.message.server.members
        discord_id = 0
        for member in members:
            if player_name == member.name:
                discord_id = member.id
        if discord_id:

            reply = sf.last_match(
                db.get_acc_id(discord_id, ctx.message.server.id),
                0, ctx)
            await self.bot.send_file(
                ctx.message.channel, 'images/lineup/lineup.png', content=reply)
            await self.bot.send_file(
                ctx.message.channel, 'images/lineup/itemlist.png')
        else:
            await self.bot.say('Invalid player name')

    @p_last.command(pass_context=True, name='full')
    async def _full(self, ctx, *, player_name):
        members = ctx.message.server.members
        discord_id = 0
        for member in members:
            if player_name == member.name:
                discord_id = member.id
        if discord_id:
            player_id = db.get_acc_id(discord_id, ctx.message.server.id)
            match_id = Player(player_id).stat_func('matches')[0]['match_id']
            post_game(match_id)
            await self.bot.send_file(ctx.message.channel, 'images/lineup/postgame.png')
        else:
            await self.bot.say('Invalid player name')

    @commands.command(pass_context=True)
    async def wr(self, ctx, *, hero_name):
        """Your winrate playing as a <hero_name>"""
        player_id = db.get_acc_id(ctx.message.author.id, ctx.message.server.id)
        try:
            hero_id = list(hero_dic.keys())[
                list(hero_dic.values()).index(hero_name)]
        except ValueError:
            await self.bot.say("Invalid hero name")
        hero_stat = Player(player_id).stat_func('wl', hero_id=hero_id)
        await self.bot.say('{0}% in {1} matches'.format(*self.winrate(hero_stat)))

    @commands.command(pass_context=True)
    async def wr_with(self, ctx, *, msg):
        """Your winrate with players (takes up to 4 arguments)"""
        names = shlex.split(msg)
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
        players_str = [str(x) for x in players]
        reply = Player(player_id).stat_func('wl', included_account_id=players_str)
        try:
            await self.bot.say('{0}% in {1} matches.'.format(*self.winrate(reply)))

        except ZeroDivisionError:
            await self.bot.say("No matches found.")

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
    async def hero_graph(self, ctx, *, hero_name):
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
        dic_records = {}
        stat_dic = (
            ('kills', 'Kills'),
            ('deaths', 'Deaths'),
            ('assists', 'Assists'),
            ('kda', 'KDA'),
            ('tower_damage', 'Tower Damage'),
            ('hero_damage', 'Hero Damage'),
            ('hero_healing', 'Hero Healing'),
            ('last_hits', 'Last Hits'),
            ('denies', 'Denies'),
            ('duration', 'Duration'),
            ('gold_per_min', 'GPM'),
            ('xp_per_min', 'XPM'),
            ('pings', 'Pings'),
            ('purchase_tpscroll', 'TPs Bought'),
            ('purchase_ward_observer', 'Obs. Wards'),
            ('purchase_rapier', 'Rapiers'))
        stat_dic = collections.OrderedDict(stat_dic)
        if hero_name:
            try:
                stat = "All-Time Records as {}:".format(hero_name[0])
                hero_id = list(hero_dic.keys())[
                    list(hero_dic.values()).index(hero_name[0])]
                reply = Player(player_id).stat_func('records', hero_id=hero_id)
                array = [['Stat', 'Value', 'Date'], ['', '', '']]  # empty line
                for entry in stat_dic.keys():
                    if entry == 'duration':
                        m, s = divmod(reply[entry][entry], 60)
                        reply[entry][entry] = '{}m {}s'.format(m, s)
                    array.append([
                        stat_dic[entry],
                        reply[entry][entry],
                        datetime.datetime.fromtimestamp(
                            int(reply[entry]['start_time'])).strftime('%d-%m-%Y')
                            ])
            except ValueError:
                await self.bot.say("Invalid hero name")
        else:
            stat = "All-Time Records:"
            reply = Player(player_id).stat_func('records')
            array = [['Stat', 'Value', 'Hero', 'Date'], ['', '', '', '']]  # empty line
            for entry in stat_dic.keys():
                if entry == 'duration':
                    m, s = divmod(reply[entry][entry], 60)
                    reply[entry][entry] = '{}m {}s'.format(m, s)
                array.append([
                    stat_dic[entry],
                    reply[entry][entry],
                    hero_dic[reply[entry]['hero_id']],
                    datetime.datetime.fromtimestamp(
                            int(reply[entry]['start_time'])).strftime('%d-%m-%Y')
                            ])

        await self.bot.say('```{}\n{}```'.format(stat, tabulate(
                array,
                tablefmt="plain",
                headers="firstrow")))

    @commands.command(pass_context=True)
    async def game_stat(self, ctx, number: int):
        """End-game screen with kda and items for all players. !game_stat 0 - your last match"""
        player_id = db.get_acc_id(ctx.message.author.id, ctx.message.server.id)

        try:
            match_id = Player(player_id).stat_func('matches')[number]['match_id']
            post_game(match_id)
        except ValueError:
            await self.bot.say("Invalid match number")
        else:
            post_game(match_id)
            await self.bot.send_file(ctx.message.channel, 'images/lineup/postgame.png')

    @commands.group(pass_context=True)
    async def mmr(self, ctx):
        """2 arguments - party/solo"""
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid sub command passed')

    @mmr.command(pass_context=True)
    async def solo(self, ctx):
        """You should have it registered on YASP"""
        players = db.get_all_ids_on_server(ctx.message.server.id)
        array = []
        for account_id in players:
            rank = Player(account_id).info()['solo_competitive_rank']
            if rank is not None:
                for member in ctx.message.server.members:
                    if db.get_discord_id(account_id, ctx.message.server.id) == member.id:
                        player_name = member.name
                array.append([player_name, int(rank)])
        leaderboard = list(sorted(array, key=lambda t: t[1], reverse=True))

        stat = 'Solo MMR leaderboard for this server:'

        await self.bot.say('```{}\n{}```'.format(stat, tabulate(
                leaderboard,
                tablefmt="plain",
                headers="firstrow")))

    @mmr.command(pass_context=True)
    async def party(self, ctx):
        players = db.get_all_ids_on_server(ctx.message.server.id)
        array = []
        for account_id in players:
            rank = Player(account_id).info()['competitive_rank']
            if rank is not None:
                for member in ctx.message.server.members:
                    if db.get_discord_id(account_id, ctx.message.server.id) == member.id:
                        player_name = member.name
                array.append([player_name, int(rank)])
        leaderboard = list(sorted(array, key=lambda t: t[1], reverse=True))

        stat = 'Party MMR leaderboard for this server:'

        await self.bot.say('```{}\n{}```'.format(stat, tabulate(
                leaderboard,
                tablefmt="plain",
                headers="firstrow")))

    @commands.command(pass_context=True)
    async def match(self, ctx, match_id: int):
        post_game(match_id)
        await self.bot.send_file(ctx.message.channel, 'images/lineup/postgame.png')


def setup(bot):
    bot.add_cog(Stats(bot))
