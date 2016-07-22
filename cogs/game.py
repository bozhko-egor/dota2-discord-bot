from discord.ext import commands
import discord
from .utils.misc import guessing_game
from random import randint
import json


class Game:

    def __init__(self, bot):
        self.bot = bot

    #@commands.command(pass_context=True)
    #async def wololo(self, ctx):
    #    await self.bot.say(ctx.message.server.id)

    @commands.command(pass_context=True)
    async def guess(self, ctx):
        """You need to guees hero you or your friend played that game"""
        server = ctx.message.server.id
        reply = guessing_game(server)
        await self.bot.send_file(
                ctx.message.channel,
                'images/lineup/itemlist2.png',
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

    @commands.group(pass_context=True)
    async def quiz(self, ctx):

        if ctx.invoked_subcommand is None:
            await bot.say('Invalid quiz command passed...')

    @quiz.command(pass_context=True)
    async def hard(self, ctx):
        with open('ref/abil_new.json') as f:
            abilities = json.load(f)

        easy_params = [
            'Cooldown',
            'Mana cost',
            'Cast range',
            'Duration',
            'Damage'
            ]
        Question = "What's the {} of the {}'s level {} {}?"
        while True:
            hero = list(abilities.keys())[randint(0, 110)]
            ability_number = randint(0, len(abilities[hero]['Abilities']) - 1)
            ability = list(abilities[hero]['Abilities'][ability_number].keys())[0]
            available_params = []
            list_of_params = list(abilities[hero]['Abilities'][ability_number][ability].keys())
            for param in list_of_params:
                if param in easy_params:
                    available_params.append(param)
            if available_params:
                break
        parameter = available_params[randint(0, len(available_params) - 1)]

        ability_array = abilities[hero]['Abilities'][ability_number][ability][parameter].split()
        lvl = randint(0, len(ability_array) - 1) + 1
        answer = int(float(ability_array[lvl - 1]))
        await self.bot.say(Question.format(parameter, hero, lvl, ability.replace('_',' ').capitalize()))

        def guess_check(m):
            return ctx.message.content

        guess = await self.bot.wait_for_message(
            timeout=7.0,
            check=guess_check,
            author=ctx.message.author,
            channel=ctx.message.channel
            )

        if guess is None:
            fmt = 'Sorry, you took too long. It was {}.'.format(answer)
            await self.bot.say(
                fmt.format(answer)
                )
            return
        if int(guess.content) == answer:

            await self.bot.say('Yay! You are right.')

        else:
            await self.bot.say(
                'Nope. It is actually {}.'.format(answer))


def setup(bot):
    bot.add_cog(Game(bot))
