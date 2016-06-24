import discord
import logging
import time
import sys
import cv2
import pymongo
import pickle
import numpy as np
from datetime import datetime, timedelta
from token_and_api_key import *
from hero_dictionary import hero_dic
from hero_dictionary import item_dic
from hero_dictionary import game_mode_dic
from random import randint
from random import shuffle

logging.basicConfig(level=logging.INFO)
client = discord.Client()
conn = pymongo.MongoClient()
db = conn['dota-db']


def my_winrate_with_player_on(player_id1, player_id2, hero_id):
        global match_search_args
        custom_args = {
            'result.players': {
                '$elemMatch': {"account_id": player_id2, "hero_id": hero_id}
            },
            'result.players.account_id': player_id1
            }
        custom_args.update(match_search_args)
        cursor = db['{}'.format(player_id1)].find(custom_args)
        hist = list(cursor)
        k = 0
        for i in range(len(hist)):
            for j in range(10):
                if hist[i]['result']['players'][j]['account_id'] == player_id1:
                    if hist[i]['result']['radiant_win'] and j < 5 or (
                            not hist[i]['result']['radiant_win'] and j > 4):
                        k += 1
        try:
            return '{}% in {} matches'.format(
                round(100*k/len(hist), 2), len(hist))
        except ZeroDivisionError:
            return 'No matches found'


def winrate_with(player_id1, player_id2):
    global match_search_args
    custom_args = {'result.players': {
        '$elemMatch': {"account_id": player_id1, "level": {'$ne': 0}}
        },
        'result.players': {
        '$elemMatch': {"account_id": player_id2, "level": {'$ne': 0}}
        }
        }
    custom_args.update(match_search_args)
    cursor = db['{}'.format(player_id1)].find(custom_args)
    hist = list(cursor)
    k = 0

    for i in range(len(hist)):
        for j in range(10):
            try:
                if hist[i]['result']['players'][j]['account_id'] == player_id1:
                    if hist[i]['result']['radiant_win'] and j < 5 or (
                            not hist[i]['result']['radiant_win'] and j > 4):
                        k += 1
            except:
                continue
    try:
        return '{}% in {} matches'.format(round(100*k/len(hist), 2), len(hist))
    except ZeroDivisionError:
        return 'No matches found'


def winrate_hero(player_id, hero_id):
    global match_search_args
    custom_args = {
            'result.players':
            {'$elemMatch': {"account_id": player_id, "hero_id": hero_id}},
            }
    custom_args.update(match_search_args)
    cursor = db['{}'.format(player_id)].find(custom_args)
    hist = list(cursor)
    k = 0
    for i in range(len(hist)):
        for j in range(10):
            if hist[i]['result']['players'][j]['account_id'] == player_id:
                if hist[i]['result']['radiant_win'] and j < 5 or (
                        not hist[i]['result']['radiant_win'] and j > 4):
                    k += 1

    try:
        return '{}% in {} matches'.format(round(100*k/len(hist), 2), len(hist))
    except ZeroDivisionError:
        return 'No matches found'


def time_diff(start_time):
    time_passed = timedelta(seconds=int(time.time() - start_time))
    d = datetime(1, 1, 1, 1, 1) + time_passed
    if d.year-1 != 0:
        return "{}y {}mo ago".format(d.year-1, d.month-1)
    else:
        if d.month-1 != 0:
            return "{}mo {}d ago".format(
                d.month-1, d.day-1)
        else:
            if d.day-1 != 0:
                return "{}d {}h ago".format(d.day-1, d.hour-1)
            else:
                return "{}h {}m ago".format(d.hour-1, d.minute-1)


def win_lose(player_id):  # in dire need of refactoring
    global match, player_index, game_status
    array3 = []
    game_type = "Solo "
    for i in range(10):
        if player_id == match['players'][i]['account_id']:
            player_index = i

        if match['players'][i]['account_id'] in list(player_dic.values()) and (
                match['players'][i]['account_id'] != player_id):
                game_type = "party with: "
                array3.append('{} ({})'.format(
                    dic_reverse[match['players'][i]['account_id']],
                    hero_dic[match['players'][i]['hero_id']]))
    game_status = game_type + ", ".join(array3)
    if (player_index > 4 and match['radiant_win']) or (
        player_index < 5 and not match['radiant_win']
    ):
        return "Lost as {}".format(
            hero_dic[match['players'][player_index]['hero_id']])
    elif (player_index > 4 and not match['radiant_win']) or (
          player_index < 5 and match['radiant_win']
    ):
        return "Won as {}".format(
            hero_dic[match['players'][player_index]['hero_id']])


def last_match(player_id, match_number):
    global match, match_search_args, hero_dic, item_dic, game_mode_dic
    custom_args = {
                'result.players.account_id': player_id}
    custom_args.update(match_search_args)
    cursor = db['{}'.format(player_id)].find(custom_args)
    cursor.sort('result.start_time', -1)
    match = list(cursor)[match_number]['result']

    stats = {}
    stats['result'] = win_lose(player_id)
    # =========================== hero images
    img_empty = cv2.imread('images/heroes/empty.png', -1)
    img_dic = {}
    array1 = []

    for j in range(10):  # объявление 10 переменных и присвоение им
        img_dic['img{}'.format(j)] = cv2.imread(  # картинки героя
            'images/heroes/{} icon.png'.format(hero_dic[
                match['players'][j]['hero_id']].lower()
                ), -1  # cv2 -flag
                                 )
        if j == 5:  # пустое изображение для пробела между командами
            array1.append(img_empty)

        array1.append(img_dic['img{}'.format(j)])

    whole_image = np.hstack(array1)
    cv2.imwrite('images/heroes/lineup/lineup.png', whole_image)
    # ================================= item images
    item_dic1 = {}
    array2 = []
    for j in range(6):
        try:
            item_dic1['img{}'.format(j)] = cv2.imread(
                'images/items/{} icon.png'.format(item_dic[
                    match['players'][player_index][
                        'item_{}'.format(j)]].lower()
                ), 1  # cv2 -flag
            )
            array2.append(item_dic1['img{}'.format(j)])
        except KeyError:  # если айтем отсутствует в слоте
            item_dic1['img{}'.format(j)] = cv2.imread(
                'images/items/empty icon.png', -1)

    whole_items = np.hstack(array2)
    cv2.imwrite('images/heroes/lineup/itemlist.png', whole_items)

    stats['game_status'] = game_status
    stats['kda'] = "{kills}/{deaths}/{assists}".format(
        **match['players'][player_index])
    stats['game_mode'] = game_mode_dic[match['game_mode']]

    stats['date'] = datetime.fromtimestamp(
        int(match['start_time'])).strftime('%d-%m-%Y %H:%M:%S')

    stats['time_passed'] = time_diff(match['start_time'])

    stats['m'], stats['s'] = divmod(match['duration'], 60)

    # dotabuff = "http://www.dotabuff.com/matches/{}".format(last_match_id)

    reply = """({game_mode}) {result} KDA: {kda}, Duration: {m}m{s}s,
        played on {date} ({time_passed}),
    {game_status}""".format(**stats)

    return reply


def avg_stats(player_id, number_of_games):
    global match_search_args
    array2 = [0]*10
    array_stat = ['kills',
                  'deaths',
                  'assists',
                  'last_hits',
                  'denies',
                  'gold_per_min',
                  'xp_per_min',
                  'hero_damage',
                  'tower_damage',
                  'level'
                  ]
    custom_args = {
                'result.players.account_id': player_id}
    custom_args.update(match_search_args)
    cursor = db['{}'.format(player_id)].find(custom_args)
    cursor.sort('result.start_time', -1)
    hist = list(cursor)
    for j in range(number_of_games):
        match = hist[j]['result']

        for i in range(10):
            if player_id == match['players'][i]['account_id']:
                player_index = i
        x = match['players'][player_index]
        for k in range(10):
            try:
                array2[k] += x[array_stat[k]]
            except:
                continue
    statList = [round(x / number_of_games, 2) for x in array2]
    return """Your avg stats in last {} games: **k**:{} **d**:{} **a**:{}, **last hits**: {}, **denies**: {}, **gpm**: {}, **xpm**: {}, **hero damage**: {}, **tower_damage**: {}, **level**: {}""".format(number_of_games, *statList)


def avg_stats_with_hero(player_id, hero_id):
    global match_search_args
    array2 = [0]*10
    array_stat = ['kills',
                  'deaths',
                  'assists',
                  'last_hits',
                  'denies',
                  'gold_per_min',
                  'xp_per_min',
                  'hero_damage',
                  'tower_damage',
                  'level'
                  ]
    custom_args = {
            'result.players':
            {'$elemMatch': {"account_id": player_id, "hero_id": hero_id}},
            }
    custom_args.update(match_search_args)
    cursor = db['{}'.format(player_id)].find(custom_args)
    hist = list(cursor)
    k = 0

    for m in range(len(hist)):
        match = hist[m]['result']
        for j in range(10):
            if hist[m]['result']['players'][j]['account_id'] == player_id:
                if hist[m]['result']['radiant_win'] and j < 5 or (
                        not hist[m]['result']['radiant_win'] and j > 4):
                    k += 1
        for i in range(10):
            if player_id == match['players'][i]['account_id']:
                player_index = i
        x = match['players'][player_index]
        for l in range(10):
            try:
                array2[l] += x[array_stat[l]]
            except:
                continue
    statList = [round(x / len(hist), 2) for x in array2]
    return """Your avg stats with {} in {} games: WR: {}% **k**:{} **d**:{} **a**:{}, **last hits**: {}, **denies**: {}, **gpm**: {}, **xpm**: {}, **hero damage**: {}, **tower_damage**: {}, **level**: {}""".format(hero_dic[hero_id], len(hist), round(100*k/len(hist), 2), *statList)


def big_pic(match_number, player_id):
    custom_args = {
                'result.players.account_id': player_id}
    custom_args.update(match_search_args)
    cursor = db['{}'.format(player_id)].find(custom_args)
    cursor.sort('result.start_time', -1)
    match = list(cursor)[match_number]['result']

    array3 = []
    for i in range(5):
        item_dic1 = {}
        array2 = []
        m = 1
        for j in range(6):
            try:
                item_dic1['img{}'.format(j)] = cv2.imread(
                    'images/items/{} icon.png'.format(item_dic[
                        match['players'][i]['item_{}'.format(j)]].lower()
                    ), 1  # cv2 -flag
                )
                array2.append(item_dic1['img{}'.format(j)])

            except KeyError:  # если айтем отсутствует в слоте
                m += 1

        for p in range(m):
            array2.append((cv2.imread(
                'images/items/empty icon.png', 1)))

        array2.insert(0, cv2.imread('images/heroes/{} icon.png'.format(hero_dic[
            match['players'][i]['hero_id']].lower()), 1))
        array2.insert(1, cv2.imread('images/vertical.png'))
        array2.insert(-1, cv2.imread('images/vertical.png'))
        array2.insert(0, cv2.imread('images/vertical.png'))
        try:
            array3.append(np.hstack(array2))
            array3.append(cv2.imread('images/346.png'))

        except:
            pass
        #cv2.imwrite('images/heroes/lineup/itemlist{}.png'.format(i), whole_items)
    array3.insert(0, (cv2.imread('images/346.png')))
    pic1 = np.vstack(array3)
    array3 = []
    for i in range(5, 10):
        item_dic1 = {}
        array2 = []

        m = 0
        for j in range(6):
            try:
                item_dic1['img{}'.format(j)] = cv2.imread(
                    'images/items/{} icon.png'.format(item_dic[
                        match['players'][i]['item_{}'.format(j)]].lower()
                    ), 1  # cv2 -flag
                )
                array2.append(item_dic1['img{}'.format(j)])

            except KeyError:  # если айтем отсутствует в слоте
                m += 1

        for p in range(m):
            array2.append((cv2.imread(
                'images/items/empty icon.png', 1)))

        array2.insert(0, cv2.imread('images/heroes/{} icon.png'.format(hero_dic[
            match['players'][i]['hero_id']].lower()), 1))
        array2.insert(1, cv2.imread('images/vertical.png'))
        array2.append(cv2.imread('images/vertical.png'))
        array2.insert(0, cv2.imread('images/vertical.png'))
        try:
            array3.append(np.hstack(array2))
            array3.append(cv2.imread('images/302.png'))

        except:
            pass
        #cv2.imwrite('images/heroes/lineup/itemlist{}.png'.format(i), whole_items)
    array3.insert(0, cv2.imread('images/302.png'))
    pic2 = np.vstack(array3)
    pic3 = np.hstack([pic1, pic2])
    cv2.imwrite('images/heroes/lineup/itemlist2.png', pic3)


def guessing_game():
    player_id = array_of_ids[randint(0, len(array_of_ids)-1)]
    custom_args = {
                'result.players.account_id': player_id}
    custom_args.update(match_search_args)
    cursor = db['{}'.format(player_id)].find(custom_args)
    cursor.sort('result.start_time', -1)
    hist = list(cursor)
    match_number = randint(0, len(hist)-1)
    match = hero_id = hist[match_number]['result']
    array3 = []
    game_type = "Solo."
    for i in range(10):
        if player_id == match['players'][i]['account_id']:
            player_index = i

        if match['players'][i]['account_id'] in list(player_dic.values()) and (
                match['players'][i]['account_id'] != player_id):
                game_type = "Party with: "
                array3.append('{}'.format(
                    dic_reverse[match['players'][i]['account_id']]))

    shuffle(array3)
    if (player_index > 4 and match['radiant_win']) or (
        player_index < 5 and not match['radiant_win']
    ):
        game_status = "Lost. " + game_type + ", ".join(array3)
    elif (player_index > 4 and not match['radiant_win']) or (
          player_index < 5 and match['radiant_win']
    ):
        game_status = "Won. " + game_type + ", ".join(array3)
    hero_id = hist[match_number]['result']['players'][player_index]['hero_id']
    hero = hero_dic[hero_id]
    big_pic(match_number, player_id)
    return [hero, dic_reverse[player_id], game_status]


@client.event
async def on_message(message):
    # do not want the bot to reply to itself
    if message.author == client.user:
        return

    # для теста
    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
        #  все пофиксить надо :(

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
                message.channel, 'images/heroes/lineup/itemlist2.png', content=reply)

    if message.content.startswith('$guess'):
        content = str(message.content).split()
        n = int(content[1])
        if 0 < n < 16:

            player_id = message.author.name
            with open('dosh.pickle', 'rb') as f:
                dosh = pickle.load(f)
            if dosh[player_id] - n >= 0:
                reply = guessing_game()
                await client.send_file(
                        message.channel, 'images/heroes/lineup/itemlist2.png', content = 'Guess a hero {} played that game. {}'.format(reply[1], reply[2]))

                def guess_check(m):
                    return message.content

                guess = await client.wait_for_message(timeout=30.0, check=guess_check, channel = message.channel)
                if guess.author == client.user:
                    guess = await client.wait_for_message(timeout=30.0, check=guess_check)
                answer = reply[0]
                if guess is None:
                    fmt = 'Sorry, you took too long. It was {}. You lost {}$'.format(answer, n)
                    dosh[player_id] -= n
                    dosh['total $ lost'] -= n
                    dosh['№ of attempts'] +=1
                    with open('dosh.pickle', 'wb') as f:
                            pickle.dump(dosh, f)
                    await client.send_message(message.channel, fmt.format(answer))
                    return
                if guess.content.lower() == answer.lower():
                    dosh[guess.author.name] += n
                    dosh['total $ won'] += n
                    dosh['№ of attempts'] +=1
                    with open('dosh.pickle', 'wb') as f:
                            pickle.dump(dosh, f)
                    await client.send_message(message.channel, 'Yay! You are right. You won {}$'.format(n))

                else:
                    dosh[guess.author.name] -= n
                    dosh['total $ lost'] -= n
                    dosh['№ of attempts'] +=1
                    with open('dosh.pickle', 'wb') as f:
                            pickle.dump(dosh, f)
                    await client.send_message(message.channel, 'Nope. It is actually {}. You lost {}$'.format(answer, n))
            else:
                await client.send_message(message.channel, "Sorry you don't have enough do$h to play this game")
        else:
            await client.send_message(message.channel, "Bets must be in [1, 15] range")
    if message.content == '!help':
        await client.send_message(message.channel, help_msg)
        # ============= only memes below ==============================================
    if message.content.startswith('%'):
        with open('dosh.pickle', 'rb') as f:
            dosh = pickle.load(f)
        if dosh[message.author.name] >= 5:
            name = str(message.content).strip().lower()[1:]
            await client.send_file(
                message.channel, 'images/twitch/{}.png'.format(name))
            dosh[message.author.name] -= 3
            with open('dosh.pickle', 'wb') as f:
                    pickle.dump(dosh, f)
        else:
            await client.send_message(message.channel, "You don't have enough dosh to post memes")
    if message.content.startswith('!new_patch'):
        await client.send_file(message.channel, 'images/new_patch.gif')
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
        await client.send_message(message.channel, "Your current balance: {}$".format(reply))
    if message.content.startswith('!total'):
        with open('dosh.pickle', 'rb') as f:
            dosh = pickle.load(f)

        await client.send_message(message.channel, "Total dosh lost:{total $ lost}$. Total dosh won: {total $ won}$. № of attempts: {№ of attempts}".format(**dosh))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(token)
