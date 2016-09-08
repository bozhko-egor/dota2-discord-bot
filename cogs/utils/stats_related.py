import cv2
import numpy as np
from .hero_dictionary import game_mode_dic
from .hero_dictionary import hero_dic
from .hero_dictionary import item_dic
from token_and_api_key import *
import time
import datetime
from .resources import db
from opendota_api.matches import Match
from opendota_api.player import Player



def time_diff(start_time):
    now = int(time.time())
    delta = now - start_time
    hours, remainder = divmod(delta, 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    if days:
        if days == 1:
            fmt = '{d} day, {h} hours, {m} minutes, and {s} seconds'
        else:
            fmt = '{d} days, {h} hours, {m} minutes, and {s} seconds'

    else:
        if hours:
            if hours == 1:
                fmt = '{h} hour, {m} minutes, and {s} seconds'
            else:
                fmt = '{h} hours, {m} minutes, and {s} seconds'

        else:
            fmt = '{m} minutes and {s} seconds'
    return fmt.format(d=days, h=hours, m=minutes, s=seconds)


def my_winrate_with_player_on(player_id1, player_id2, hero_id):
        matches = Player(player_id1).stat_func(
                'matches',
                included_account_id=player_id2,
                with_hero_id=hero_id
                )
        all_matches = 0
        won_matches = 0
        position_list = [
            '0',
            '1',
            '2',
            '3',
            '4',
            '128',
            '129',
            '130',
            '131',
            '132'
            ]
        for match in matches:
            for entry in position_list:
                try:
                    if (match['heroes'][entry]['account_id'] == player_id2 and
                        match['heroes'][entry]['hero_id'] == hero_id):

                        all_matches += 1
                except KeyError:
                    pass
        hist2 = Player(player_id1).stat_func(
                'matches',
                included_account_id=player_id2,
                with_hero_id=hero_id,
                win=1
                )

        for match in hist2:
            for entry in position_list:
                try:
                    if (match['heroes'][entry]['account_id'] == player_id2 and
                        match['heroes'][entry]['hero_id'] == hero_id):

                        won_matches += 1
                except KeyError:
                    pass

        try:
            return '{}% in {} matches'.format(
                round(100*won_matches/all_matches, 2), all_matches)
        except ZeroDivisionError:
            return 'No matches found'


def win_lose(player_id, match, ctx):  # in dire need of refactoring
    global player_index, game_status
    array3 = []
    game_type = "Solo "
    ids = db.get_all_ids_on_server(ctx.message.server.id)
    for i in range(10):
        if player_id == match['players'][i]['account_id']:
            player_index = i

        if match['players'][i]['account_id'] in ids and (
                match['players'][i]['account_id'] != player_id):
                game_type = "Party with: "
                discord_id = db.get_discord_id(match['players'][i]['account_id'], ctx.message.server.id)
                for member in ctx.message.server.members:
                    if discord_id == member.id:
                        player_name = member.name
                array3.append('{}'.format(player_name))
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


def last_match(player_id, match_number, ctx):
    global player_index, game_status
    match_id = Player(player_id).stat_func('matches')[match_number]['match_id']
    match = Match(match_id).info()
    stats = {}
    stats['result'] = win_lose(player_id, match, ctx)
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
    cv2.imwrite('images/lineup/lineup.png', whole_image)
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
    cv2.imwrite('images/lineup/itemlist.png', whole_items)

    stats['game_status'] = game_status
    stats['kda'] = "{kills}/{deaths}/{assists}".format(
        **match['players'][player_index])
    stats['game_mode'] = game_mode_dic[match['game_mode']]

    stats['date'] = datetime.datetime.fromtimestamp(
        int(match['start_time'])).strftime('%d-%m-%Y %H:%M:%S')

    stats['time_passed'] = time_diff(match['start_time'])

    stats['m'], stats['s'] = divmod(match['duration'], 60)

    # dotabuff = "http://www.dotabuff.com/matches/{}".format(last_match_id)

    reply = """{result}, KDA: {kda}, {game_status}""".format(**stats)
    #reply = reply.replace('\n', ' ')
    return reply


def avg_stats(player_id, number_of_games):
    array2 = [0]*8
    array_stat = ['kills',
                  'deaths',
                  'assists',
                  'last_hits',
                  'denies',
                  'gold_per_min',
                  'xp_per_min',
                  'level'
                  ]
    args = {'players.account_id': player_id}
    hist = db.get_match_list(args)
    for j in range(number_of_games):
        match = hist[j]

        for i in range(10):
            if player_id == match['players'][i]['account_id']:
                player_index = i
        x = match['players'][player_index]
        for k in range(8):
            try:
                array2[k] += x[array_stat[k]]
            except:
                continue
    statList = [round(x / number_of_games, 2) for x in array2]
    reply = """Your avg stats in last {} games: **k**:{} **d**:{} **a**:{},
**last hits**: {}, **denies**: {}, **gpm**: {}, **xpm**: {},
**level**: {}""".format(number_of_games, *statList)
    reply = reply.replace('\n', ' ')
    return reply


def avg_stats_with_hero(player_id, hero_id):
    array2 = [0]*8
    array_stat = ['kills',
                  'deaths',
                  'assists',
                  'last_hits',
                  'denies',
                  'gold_per_min',
                  'xp_per_min',
                  'level'
                  ]
    args = {'players':
            {'$elemMatch': {"account_id": player_id, "hero_id": hero_id}},
            }

    hist = db.get_match_list(args)
    k = 0

    for m, game in enumerate(hist):
        match = game
        for j in range(10):
            if match['players'][j]['account_id'] == player_id:
                if match['radiant_win'] and j < 5 or (
                        not match['radiant_win'] and j > 4):
                    k += 1
        for i in range(10):
            if player_id == match['players'][i]['account_id']:
                player_index = i
        x = match['players'][player_index]
        for l in range(8):
            try:
                array2[l] += x[array_stat[l]]
            except:
                continue
    statList = [round(x / len(hist), 2) for x in array2]
    reply = """Your avg stats with {} in {} games: WR: {}%,
**k**:{} **d**:{} **a**:{}, **last hits**: {}, **denies**: {},
**gpm**: {}, **xpm**: {},
**level**: {}""".format(
          hero_dic[hero_id], len(hist), round(100*k/len(hist), 2), *statList)
    reply = reply.replace('\n', ' ')
    return reply
