from discord.ext import commands
import discord
from .utils import stat_func, checks
import os

class Meta:
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def uptime(self):
        """Bot's current uptime"""
        reply = stat_func.time_diff(self.bot.uptime)
        await self.bot.say(reply)

    @commands.command()
    async def join(self):
        """Joins a server."""
        perms = discord.Permissions.none()
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

def setup(bot):
    bot.add_cog(Meta(bot))
