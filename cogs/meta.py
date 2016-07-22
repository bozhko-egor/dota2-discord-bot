from discord.ext import commands
import discord
from .utils import stat_func, checks


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


def setup(bot):
    bot.add_cog(Meta(bot))
