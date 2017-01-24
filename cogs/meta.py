from discord.ext import commands
import discord
from .utils import stats_related, checks
import os
from .utils.resources import db
from csv import reader
import shlex
from token_and_api_key import log_chat_id
from cogs.utils.hero_dictionary import hero_dic
from collections import Counter

class Meta:

    def __init__(self, bot):
        self.bot = bot

    def get_discord_id(self, ctx, name):
        discord_id = 0
        for member in ctx.message.server.members:
            if name == member.name:
                discord_id = member.id
        return discord_id

    @commands.command(pass_context=True)
    async def wololo(self, ctx):
        message = await self.bot.say('0')
        for i in range(1, 100):
            await self.bot.edit_message(message, '{}'.format(i))

    @commands.command()
    async def uptime(self):
        """Bot's current uptime"""
        reply = stats_related.time_diff(self.bot.uptime)
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
        result.append('- Author: Egor#5310 (Discord ID: 134716781750124544)')
        result.append('- Library: discord.py (Python)')
        result.append('- Source code : https://github.com/bozhko-egor/dota2-discord-bot')
        result.append('- Latest Change: {}'.format(revision))
        result.append('- Uptime: {}'.format(stats_related.time_diff(self.bot.uptime)))
        result.append('- Servers: {}'.format(len(self.bot.servers)))
        result.append('- Commands Run: {}'.format(self.bot.commands_used))
        total_members = sum(len(s.members) for s in self.bot.servers)

        total_online = sum(1 for m in self.bot.get_all_members() if m.status != discord.Status.offline)
        unique_members = set(self.bot.get_all_members())
        unique_online = sum(1 for m in unique_members if m.status != discord.Status.offline)
        channel_types = Counter(c.type for c in self.bot.get_all_channels())
        voice = channel_types[discord.ChannelType.voice]
        text = channel_types[discord.ChannelType.text]
        result.append('- Total Members: {} ({} online)'.format(total_members, total_online))
        result.append('- Unique Members: {} ({} online)'.format(len(unique_members), unique_online))
        result.append('- {} text channels, {} voice channels'.format(text, voice))
        result.append('')
        await self.bot.say('\n'.join(result))

    @commands.command(hidden=True, pass_context=True)
    @checks.is_owner()
    async def add_player(self, ctx, steamid: int, *, player_name):
            discord_id = self.get_discord_id(ctx, player_name)
            if discord_id:
                db.add_id(discord_id, ctx.message.server.id, steamid)
                await self.bot.say('Done!')
            else:
                await self.bot.say('Invalid player name')

    @commands.command(hidden=True, pass_context=True)
    @checks.is_owner()
    async def delete_player(self, ctx, *, player_name):
        discord_id = self.get_discord_id(ctx, player_name)
        if discord_id:
            reply = db.delete_id(discord_id, ctx.message.server.id)
            if reply:
                await self.bot.say(reply)
            else:
                await self.bot.say("Done!")
        else:
            await self.bot.say('Invalid player name')

    @commands.command(pass_context=True, no_pm=True)
    async def add_steamid(self, ctx, steamid: str):
        """Makes connection discord id - steam id"""
        if steamid.isdigit():
            discord_id = ctx.message.author.id
            reply = db.add_id(discord_id, ctx.message.server.id, int(steamid))
            if reply:
                await self.bot.say(reply)
            else:
                await self.bot.say("Done!")
        else:
            await self.bot.say("Invalid input.")
    @commands.command(pass_context=True, no_pm=True)
    async def delete_steamid(self, ctx):
        discord_id = ctx.message.author.id
        reply = db.delete_id(discord_id, ctx.message.server.id)
        if reply:
            await self.bot.say(reply)
        else:
            await self.bot.say("Done!")

    @commands.command(name='quit', hidden=True)
    @checks.is_owner()
    async def _quit(self):
        """Quits the bot."""
        await self.bot.logout()

    @commands.command(pass_context=True)
    async def get_history(self, ctx):
        channel = ctx.message.channel
        logs = self.bot.logs_from(channel, limit=100000)
        name = 'logs{}-{}.txt'.format(channel.name, channel.server.name)
        with open(name, 'a') as f:
            async for i in logs:
                f.write('{} {} - {}\n'.format(i.timestamp, i.author.name, i.content))
        await self.bot.send_file(ctx.message.channel, name)

        await self.bot.say("lol")

def setup(bot):
    bot.add_cog(Meta(bot))
