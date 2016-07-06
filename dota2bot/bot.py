import discord
import logging
import sys
from stat_func import *
from misc import *
import time
import pymongo
import pickle
from token_and_api_key import *
from recent_games_parser import get_recent_matches
from hero_dictionary import hero_dic
from hero_dictionary import item_dic
from hero_graph import hero_per_month

logging.basicConfig(level=logging.INFO)
client = discord.Client()
launch_time = int(time.time())




if not discord.opus.is_loaded():

    discord.opus.load_opus('/usr/local/lib/libopusfile.so')

@client.event
async def on_message(message):

        # do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!last'):
        player_id = player_dic[message.author.name]
        if message.content == '!last':
            reply = '{0.author.mention} {1}'.format(
                message, last_match(player_id, 0))
        else:
            content = str(message.content).split()
            match_number = int(content[1])
            reply = '{0.author.mention} {1}'.format(
                message, last_match(player_id, match_number))
        await client.send_file(
            message.channel, 'images/heroes/lineup/lineup.png', content=reply)
        await client.send_file(
            message.channel, 'images/heroes/lineup/itemlist.png')

    if message.content.startswith('!p_last'):
        content = str(message.content).split()
        if len(content) == 2:
            match_number = 0
            player_id = player_dic[content[1]]
            reply = last_match(player_id, match_number)
        elif len(content) == 3:
            player_id = player_dic[content[2]]
            match_number = int(content[1])
            reply = last_match(player_id, match_number)

        await client.send_file(
            message.channel, 'images/heroes/lineup/lineup.png', content=reply)
        await client.send_file(
            message.channel, 'images/heroes/lineup/itemlist.png')

    if message.content.startswith('!stats'):
        content = str(message.content).split()
        n = int(content[1])
        player_id = player_dic[message.author.name]
        stats = avg_stats(player_id, n)
        await client.send_message(message.channel, stats)

    if message.content.startswith('!wr '):
        content = str(message.content).split()
        if len(content) == 3:
            hero_name = ' '.join(content[1: 3])
        elif len(content) == 2:
            hero_name = content[1]

        player_id = player_dic[message.author.name]
        hero_id = list(hero_dic.keys())[
            list(hero_dic.values()).index(hero_name)]
        reply = winrate_hero(player_id, hero_id)
        await client.send_message(message.channel, reply)

    if message.content.startswith('!wr_with '):
        content = str(message.content).split()
        player_id = player_dic[message.author.name]
        name = content[1]
        player_id2 = player_dic[name]
        reply = winrate_with(player_id, player_id2)
        await client.send_message(message.channel, reply)

    if message.content.startswith('!wr_with_hero'):
        content = str(message.content).split()
        if len(content) == 4:
            hero_name = ' '.join(content[2: 4])
        elif len(content) == 3:
            hero_name = content[2]
        player_id = player_dic[message.author.name]
        name = content[1]
        player_id2 = player_dic[name]
        hero_id = list(hero_dic.keys())[list(
            hero_dic.values()).index(hero_name)]
        reply = my_winrate_with_player_on(player_id, player_id2, hero_id)
        await client.send_message(message.channel, reply)

    # except ValueError:
    #    await client.send_message(
    #       message.channel, " :(")
    if message.content.startswith('!avg_stats'):
        content = str(message.content).split()
        player_id = player_dic[message.author.name]
        if len(content) == 3:
            hero_name = ' '.join(content[1: 3])
        elif len(content) == 2:
            hero_name = content[1]
        hero_id = list(hero_dic.keys())[
            list(hero_dic.values()).index(hero_name)]
        reply = '{0.author.mention} {1}'.format(
            message, avg_stats_with_hero(player_id, hero_id))
        await client.send_message(message.channel, reply)

    if message.content.startswith('?last'):
        player_id = player_dic[message.author.name]
        if message.content == '?last':
            reply = last_match(player_id, 0)
            big_pic(0, player_id)
        else:
            content = str(message.content).split()
            match_number = int(content[1])
            reply = last_match(player_id, match_number)
            big_pic(match_number, player_id)
        await client.send_file(
                message.channel,
                'images/heroes/lineup/itemlist2.png',
                content=reply
                )

    if message.content.startswith('$guess'):
        content = str(message.content).split()
        n = int(content[1])
        if 0 < n <= 15:

            player_id = message.author.name
            with open('dosh.pickle', 'rb') as f:
                dosh = pickle.load(f)
            if dosh[player_id] - n >= 0:
                reply = guessing_game()
                await client.send_file(
                        message.channel,
                        'images/heroes/lineup/itemlist2.png',
                        content='Guess a hero {} played that game. {}'.format(
                            reply[1], reply[2])
                        )

                def guess_check(m):
                    return message.content

                guess = await client.wait_for_message(
                    timeout=30.0,
                    check=guess_check,
                    author=message.author,
                    channel=message.channel
                    )
                answer = reply[0]
                if guess is None:
                    fmt = 'Sorry, you took too long. It was {}. You lost {}$'.format(answer, n)
                    dosh[player_id] -= n
                    dosh['total $ lost'] -= n
                    dosh['№ of attempts'] += 1
                    with open('dosh.pickle', 'wb') as f:
                            pickle.dump(dosh, f)
                    await client.send_message(
                        message.channel,
                        fmt.format(answer)
                        )
                    return
                if guess.content.lower() == answer.lower():
                    dosh[guess.author.name] += n
                    dosh['total $ won'] += n
                    dosh['№ of attempts'] += 1
                    with open('dosh.pickle', 'wb') as f:
                            pickle.dump(dosh, f)
                    await client.send_message(
                        message.channel,
                        'Yay! You are right. You won {}$'.format(n)
                        )

                else:
                    dosh[guess.author.name] -= n
                    dosh['total $ lost'] -= n
                    dosh['№ of attempts'] += 1
                    with open('dosh.pickle', 'wb') as f:
                            pickle.dump(dosh, f)
                    await client.send_message(
                        message.channel,
                        'Nope. It is actually {}. You lost {}$'.format(answer, n))
            else:
                await client.send_message(
                    message.channel,
                    "Sorry you don't have enough do$h to play this game"
                    )
        else:
            await client.send_message(message.channel, "Bets must be in [1, 15] range")
    if message.content == '!help':
        await client.send_message(message.channel, help_msg)
        # ============= only memes below ======================================
    if message.content.startswith('%'):
        with open('dosh.pickle', 'rb') as f:
            dosh = pickle.load(f)
        if dosh[message.author.name] >= 3:
            name = str(message.content).strip().lower()[1:]
            await client.send_file(
                message.channel, 'images/twitch/{}.png'.format(name))
            dosh[message.author.name] -= 3
            with open('dosh.pickle', 'wb') as f:
                    pickle.dump(dosh, f)
        else:
            await client.send_message(
                message.channel,
                "You don't have enough dosh to post memes"
                )
    if message.content.startswith('!new_patch'):
        await client.send_file(message.channel, 'images/twitch/new_patch.gif')
        await client.change_status(game=discord.Game(name='DOTA2'))

    if message.content.startswith('!hero'):
        name = str(message.content).strip().lower()[6:]
        await client.send_file(
            message.channel, 'images/heroes/{} icon.png'.format(name))

    if message.content.startswith('!item'):
        name = str(message.content).strip().lower()[6:]
        await client.send_file(
            message.channel, 'images/items/{} icon.png'.format(name))

    if message.content.startswith('!nice'):
        await client.send_file(message.channel, 'images/twitch/nice.gif')
        await client.change_status(game=discord.Game(name='Nice'))

    if message.content.startswith('!balance'):
        with open('dosh.pickle', 'rb') as f:
            dosh = pickle.load(f)
        reply = dosh[message.author.name]
        await client.send_message(
            message.channel,
            "Your current balance: {}$".format(reply)
            )
    if message.content.startswith('!total'):
        with open('dosh.pickle', 'rb') as f:
            dosh = pickle.load(f)

        await client.send_message(message.channel, "Total dosh lost:{total $ lost}$. Total dosh won: {total $ won}$. № of attempts: {№ of attempts}".format(**dosh))

    if message.content.startswith('#'):
        player_id = message.author
        with open('dosh.pickle', 'rb') as f:
            dosh = pickle.load(f)
        if dosh[message.author.name] >= 5:
            name = str(message.content).strip().lower()[1:]
            voice = await  client.join_voice_channel(player_id.voice_channel)
            if message.content.startswith('#hs'):
                player = voice.create_ffmpeg_player('audio/{}.ogg'.format(name))
            else:
                player = voice.create_ffmpeg_player('audio/{}.mp3'.format(name))

            player.start()

            time.sleep(5)
            player.stop()
            await voice.disconnect()
            dosh[message.author.name] -= 5
            with open('dosh.pickle', 'wb') as f:
                    pickle.dump(dosh, f)
        else:
            await client.send_message(message.channel, "You don't have enough dosh to post memes")

    if message.content.startswith('$roulette'):
        content = str(message.content).split()
        n = int(content[1])
        player_id = message.author.name
        with open('dosh.pickle', 'rb') as f:
            dosh = pickle.load(f)
        if 0 < n <= 30:
            if dosh[player_id] - n >= 0:
                reply = roulette(n, dosh, player_id)
                await client.send_message(message.channel, reply)
            else:
                await client.send_message(message.channel, "You don't have enough dosh.")
        else:
            await client.send_message(message.channel, "Bets must be in (0, 30] range")

    if message.content.startswith('!update'):
        if message.author.id in bot_admin:
            reply = get_recent_matches()
            await client.send_message(
                message.channel, reply)
        else:
            await client.send_message(
              message.channel, "You need permission to perform this action")

    if message.content.startswith('!graph_hero'):
        content = str(message.content).split()
        if len(content) == 3:
            hero_name = ' '.join(content[1: 3])
        elif len(content) == 2:
            hero_name = content[1]

        player_id = player_dic[message.author.name]
        hero_id = list(hero_dic.keys())[
            list(hero_dic.values()).index(hero_name)]
        reply = hero_per_month(player_id, hero_id)
        await client.send_file(
                message.channel, 'images/graphs/hero.png', content=reply)
    if message.content.startswith('!channel'):

        await client.send_message(message.channel, str(message.channel))

    if message.content == '!uptime':
        uptime = time_diff(launch_time)
        await client.send_message(message.channel, uptime)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(token)
