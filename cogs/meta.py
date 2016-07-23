from discord.ext import commands
import discord
from .utils import stat_func, checks
import os
from .utils.resources import db
from csv import reader
class Meta:

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def uptime(self):
        """Bot's current uptime"""
        reply = stat_func.time_diff(self.bot.uptime)
        await self.bot.say(reply)

    @commands.command(pass_context=True)
    async def wololo(self, ctx, *, msg):
        players = []

        for line in reader([repr(msg)], skipinitialspace=True):
            players.append(line)
        #array = []
        #members = ctx.message.server.members
        #for member in members:
        #    if name == member.name:
        #        array.append(member.id)
        await self.bot.say(players)

    @commands.command()
    async def join(self):
        """Joins a server."""
        perms = dhidden=Trueiscord.Permissions.none()
        perms.read_messages = True
        perms.send_messages = True
        perms.manage_roles = True
        perms.ban_members = True
        perms.kick_members = True
        perms.manage_messages = True
        perms.embed_links = True
        perms.read_message_history = True
        perms.attach_files = True
        await self.bot.say(discord.utils.oauth_url(self.bot.client_id, perms))

    @commands.command()
    async def about(self):
        """Tells you information about the bot itself."""
        revision = os.popen(r'git show -s HEAD --format="%s (%cr)"').read().strip()
        result = ['**About Me:**']
        result.append('- Author: Егор#5310 (Discord ID: 134716781750124544)')
        result.append('- Library: discord.py (Python)')
        result.append('- Source code : https://github.com/bozhko-egor/dota2-discord-bot')
        result.append('- Latest Change: {}'.format(revision))
        result.append('- Uptime: {}'.format(stat_func.time_diff(self.bot.uptime)))
        await self.bot.say('\n'.join(result))

    @commands.command(hidden=True, pass_context=True)
    @checks.is_owner()
    async def add_player(self, ctx, steamid: int, *, player_name):
            discord_id = 0
            for member in ctx.message.server.members:
                if player_name == member.name:
                    discord_id = member.id
            if discord_id:
                db.add_id(discord_id, ctx.message.server.id, steamid)
                await self.bot.say('Done!')
            else:
                await self.bot.say('Invalid player name')

def setup(bot):
    bot.add_cog(Meta(bot))
