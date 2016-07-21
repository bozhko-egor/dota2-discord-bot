from discord.ext import commands
import discord
from misc import guessing_game

class Game:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def guess(self, ctx):
        """You need to guees hero you or your friend played that game"""
        reply = guessing_game()
        await self.bot.send_file(
                ctx.message.channel,
                'images/heroes/lineup/itemlist2.png',
                content='Guess a hero {} played that game. {}'.format(
                    reply[1], reply[2])
                )

        def guess_check(m):
            return ctx.message.content

        guess = await self.bot.wait_for_message(
            timeout=30.0,
            check=guess_check,
            author=ctx.message.author,
            channel=ctx.message.channel
            )
        answer = reply[0]
        if guess is None:
            fmt = 'Sorry, you took too long. It was {}.'.format(answer)
            await self.bot.send_message(
                ctx.message.channel,
                fmt.format(answer)
                )
            return
        if guess.content.lower() == answer.lower():

            await self.bot.say('Yay! You are right.')

        else:
            await self.bot.say(
                'Nope. It is actually {}.'.format(answer))


def setup(bot):
    bot.add_cog(Game(bot))
