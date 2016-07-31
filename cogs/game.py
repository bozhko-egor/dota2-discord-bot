from discord.ext import commands
import discord
from .utils.misc import guessing_game
from random import randint
import json
from .utils.resources import db
import datetime


class Game:

    def __init__(self, bot):
        self.bot = bot

    #@commands.command(pass_context=True)
    #async def wololo(self, ctx):
    #    await self.bot.say(ctx.message.server.id)
    def get_name(self, ctx, discord_id):
        name = ''
        for member in ctx.message.server.members:
            if discord_id == member.id:
                name = member.name
        return name

    @commands.group(pass_context=True)
    async def leaderboard(self, ctx):
        if ctx.invoked_subcommand is None:
            await bot.say('Invalid subcommand passed')

    @leaderboard.command(pass_context=True, name='guess')
    async def _guess(self, ctx):
        """Leaderboard for !guess game"""
        reply = '\n'
        for i, entry in enumerate(db.get_leaderboard(
                ctx.message.server.id,
                'guess-leaderboard')):
            for key, value in entry.items():
                if key == "discord_id":
                    name = self.get_name(ctx, value)
                elif key == 'date':
                    date = value
                else:
                    score = value
            reply += '{}. {} - {} ({})\n'.format(
                i+1,
                score,
                name,
                datetime.datetime.fromtimestamp(
                    int(date)).strftime('%d-%m-%Y')
                )
        await self.bot.say(reply)

    @leaderboard.command(pass_context=True, name='quiz-easy')
    async def _quiz1(self, ctx):
        """Leaderboard for quiz-easy game"""
        reply = '\n'
        for i, entry in enumerate(db.get_leaderboard(
                ctx.message.server.id,
                'quizeasy-leaderboard')):
            for key, value in entry.items():
                if key == "discord_id":
                    name = self.get_name(ctx, value)
                elif key == 'date':
                    date = value
                else:
                    score = value
            reply += '{}. {} - {} ({})\n'.format(
                i+1,
                score,
                name,
                datetime.datetime.fromtimestamp(
                    int(date)).strftime('%d-%m-%Y')
                )
        await self.bot.say(reply)

    @commands.command(pass_context=True)
    async def guess(self, ctx):
        """You need to guess hero you or your friend played that game"""
        server = ctx.message.server.id
        current_streak = 0
        while True:
            if current_streak > 0:
                await self.bot.say('Your current streak is {}'.format(current_streak))
            reply = guessing_game(server, ctx)
            await self.bot.send_file(
                    ctx.message.channel,
                    'images/lineup/game_postgame.png',
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
                fmt = 'Sorry, you took too long. It was {}.\nGame over. Your score: {}.'
                await self.bot.send_message(
                    ctx.message.channel,
                    fmt.format(answer, current_streak)
                    )
                if current_streak > 0:
                    db.add_leaderboard_guess(
                        ctx.message.server.id,
                        ctx.message.author.id,
                        current_streak,
                        'guess-leaderboard'
                        )
                break
            if guess.content.lower() == answer.lower():

                await self.bot.say('Yay! You are right.')
                current_streak += 1
            else:
                await self.bot.say(
                    'Nope. It is actually {}.\n Game over. Your score: {}'.format(answer, current_streak))
                if current_streak > 0:
                    db.add_leaderboard_guess(
                        ctx.message.server.id,
                        ctx.message.author.id,
                        current_streak,
                        'guess-leaderboard'
                        )
                break


    @commands.group(pass_context=True)
    async def quiz(self, ctx):

        if ctx.invoked_subcommand is None:
            await bot.say('Invalid quiz command passed...')

    @quiz.command(pass_context=True)
    async def easy(self, ctx):
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
        current_streak = 0
        pct_ = 0.25
        while True:
            pct_ = pct_ - 0.05 if current_streak > 2 and current_streak % 3 == 0 and pct_ != 0 else pct_
            if current_streak > 0:
                await self.bot.say('Your current streak is {}'.format(current_streak))
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
            await self.bot.say(Question.format(parameter, hero, lvl, ability.replace('_', ' ').capitalize()))

            def guess_check(m):
                return ctx.message.content

            guess = await self.bot.wait_for_message(
                timeout=10.0,
                check=guess_check,
                author=ctx.message.author,
                channel=ctx.message.channel
                )

            if guess is None:
                fmt = 'Sorry, you took too long. It was {}.\n Game over. Your score: {}'.format(answer, current_streak)
                await self.bot.say(
                    fmt.format(answer)
                    )
                if current_streak > 0:
                    db.add_leaderboard_guess(
                        ctx.message.server.id,
                        ctx.message.author.id,
                        current_streak,
                        'quizeasy-leaderboard'
                        )
                break

            if pct_*answer < pct_*100/5:
                increment = pct_*20
            else:
                increment = answer * pct_

            try:
                int(guess.content)
            except ValueError:
                await self.bot.say('Nope. It is actually {} +-{}.\n Game over. Your score:{}'.format(answer, pct_*answer, current_streak))
                break
            if answer - increment <= int(guess.content) <= answer + increment:
                await self.bot.say('Yay! You are right.({})'.format(answer))
                current_streak += 1
            else:
                await self.bot.say(
                    'Nope. It is actually {} +-{}.\n Game over. Your score:{}'.format(answer, pct_*answer, current_streak))
                if current_streak > 0:
                    db.add_leaderboard_guess(
                        ctx.message.server.id,
                        ctx.message.author.id,
                        current_streak,
                        'quizeasy-leaderboard'
                        )
                break

def setup(bot):
    bot.add_cog(Game(bot))
