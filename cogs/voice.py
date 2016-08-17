from discord.ext import commands
import discord
import os
import time


class Voice:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def voice(self, ctx, *, voice_line):
        """Plays voice line into your current voice channel. No spam pls. Valid voice commands:
        am/jugg/lich/lich2/noice/shaker/shaker2/wd/wd2/wl/wow"""
        if os.path.isfile('audio/{}.mp3'.format(voice_line)):
                user = ctx.message.author
                voice = await self.bot.join_voice_channel(user.voice_channel)
                player = voice.create_ffmpeg_player('audio/{}.mp3'.format(voice_line))
                player.start()
                time.sleep(4)   # need to change that
                player.stop()
                await voice.disconnect()
        else:
            await self.bot.say('Invalid voice line')




def setup(bot):
    bot.add_cog(Voice(bot))
