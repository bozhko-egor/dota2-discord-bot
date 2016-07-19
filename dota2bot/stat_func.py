import pymongo
import cv2
import numpy as np
from hero_dictionary import game_mode_dic
from hero_dictionary import hero_dic
from hero_dictionary import item_dic
from token_and_api_key import *
import time
from datetime import datetime, timedelta

conn = pymongo.MongoClient()
db = conn['dota2-db']

match_search_args = {
            'game_mode': {'$in': [0, 1, 2, 3, 4, 5, 12, 14, 16, 22]},
            'duration': {'$gt': 720},
            'players.level': {'$nin': [1, 2, 3]},
            'players.leaver_status': {'$nin': [5, 6]},
            'lobby_type': {'$in': [0, 5, 6, 7]}
            }


def time_diff(start_time):
    time_passed = timedelta(seconds=int(time.time() - start_time))
    d = datetime(1, 1, 1, 1, 1, 1) + time_passed
    if d.year-1 != 0:
        return "{}y {}mo".format(d.year-1, d.month-1)
    else:
        if d.month-1 != 0:
            return "{}mo {}d".format(
                d.month-1, d.day-1)
        else:
            if d.day-1 != 0:
                return "{}d {}h".format(d.day-1, d.hour-1)
            else:
                if d.hour-1 != 0:
                    return "{}h {}m".format(d.hour-1, d.minute-1)
                else:
                    return "{}m {}s".format(d.minute-1, d.second-1)



def my_winrate_with_player_on(player_id1, player_id2, hero_id):
        global match_search_args
        custom_args = {
            'players': {
                '$elemMatch': {"account_id": player_id2, "hero_id": hero_id}
            },
            'players.account_id': player_id1
            }
        custom_args.update(match_search_args)
        cursor = db['matches_all'].find(custom_args)
        hist = list(cursor)
        k = 0
        for i, game in enumerate(hist):
            for j in range(10):
                if game['players'][j]['account_id'] == player_id1:
                    if game['radiant_win'] and j < 5 or (
                            not game['radiant_win'] and j > 4):
                        k += 1
        try:
            return '{}% in {} matches'.format(
                round(100*k/len(hist), 2), len(hist))
        except ZeroDivisionError:
            return 'No matches found'


def winrate_with(player_id1, names):
    global match_search_args
    ids = [
        {'players.account_id': player_id1}
        ]
    custom_args = {'$and': ids}
    if len(names) == 0 or len(names) > 4:
        return "Please enter valid number of names"
    else:
        for player_id in names:
            ids.append({'players.account_id': player_id})
    custom_args = {'$and': ids}
    custom_args.update(match_search_args)
    cursor = db['matches_all'].find(custom_args)
    hist = list(cursor)
    k = 0

    for i, game in enumerate(hist):
        for j in range(10):
            try:
                if game['players'][j]['account_id'] == player_id1:
                    if game['radiant_win'] and j < 5 or (
                            not game['radiant_win'] and j > 4):
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
            'players':
            {'$elemMatch': {"account_id": player_id, "hero_id": hero_id}},
            }
    custom_args.update(match_search_args)
    cursor = db['matches_all'].find(custom_args)
    hist = list(cursor)
    k = 0
    for i, game in enumerate(hist):
        for j in range(10):
            if game['players'][j]['account_id'] == player_id:
                if game['radiant_win'] and j < 5 or (
                        not game['radiant_win'] and j > 4):
                    k += 1

    try:
        return '{}% in {} matches'.format(round(100*k/len(hist), 2), len(hist))
    except ZeroDivisionError:
        return 'No matches found'
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
                'players.account_id': player_id}
    custom_args.update(match_search_args)
    cursor = db['matches_all'].find(custom_args)
    cursor.sort('start_time', -1)
    match = list(cursor)[match_number]

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
    played on {date} ({time_passed} ago), {game_status}""".format(**stats)
    reply = reply.replace('\n', ' ')
    return reply


def avg_stats(player_id, number_of_games):
    global match_search_args
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
    custom_args = {
                'players.account_id': player_id}
    custom_args.update(match_search_args)
    cursor = db['matches_all'].find(custom_args)
    cursor.sort('start_time', -1)
    hist = list(cursor)
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
    global match_search_args
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
    custom_args = {
            'players':
            {'$elemMatch': {"account_id": player_id, "hero_id": hero_id}},
            }
    custom_args.update(match_search_args)
    cursor = db['matches_all'].find(custom_args)
    hist = list(cursor)
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


def big_pic(player_id, match_number):
    custom_args = {
                'players.account_id': player_id}
    custom_args.update(match_search_args)
    cursor = db['matches_all'].find(custom_args)
    cursor.sort('start_time', -1)
    match = list(cursor)[match_number]

    array3 = []
    # radiant team
    for i in range(5):
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
        # append all empty slots in the end of inventory
        for p in range(m):
            array2.append((cv2.imread(
                'images/items/empty icon.png', 1)))
        array2.insert(0, cv2.imread('images/vertical.png'))
        # hero pic
        array2.insert(0, cv2.imread('images/heroes/{} icon.png'.format(hero_dic[
            match['players'][i]['hero_id']].lower()), 1))
        array2.insert(1, cv2.imread('images/vertical.png'))

        kda = ['kills', 'deaths', 'assists']
        kda_values = [0]*3
        for number, stat in enumerate(kda):
            if len(str(match['players'][i][stat])) == 2:
                kda_values[number] = str(match['players'][i][stat])
            else:
                kda_values[number] = '&{}&'.format(str(match['players'][i][stat]))
        kda_values.insert(1, '-')
        kda_values.insert(3, '-')
        kda_values = ''.join(kda_values)
        symbols = list(kda_values)
        kda_array = []
        for q, element in enumerate(symbols):
            array2.insert(2+q, cv2.imread('images/numbers/{}.png'.format(element)))
        #array2.insert(10, cv2.imread('images/vertical.png'))
        array2.append(cv2.imread('images/vertical.png'))
        array2.insert(0, cv2.imread('images/vertical.png'))

        try:
            array3.append(np.hstack(array2))
            array3.append(cv2.imread('images/448.png'))

        except:
            pass

        #cv2.imwrite('images/heroes/lineup/itemlist{}.png'.format(i), whole_items)
    array3.insert(0, (cv2.imread('images/448.png')))
    array3.append(cv2.imread('images/448_big.png'))
    pic1 = np.vstack(array3)

    # dire team
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
        array2.insert(0, cv2.imread('images/vertical.png'))
        array2.insert(0, cv2.imread('images/heroes/{} icon.png'.format(hero_dic[
            match['players'][i]['hero_id']].lower()), 1))
        array2.insert(1, cv2.imread('images/vertical.png'))
        kda = ['kills', 'deaths', 'assists']
        kda_values = [0]*3
        for number, stat in enumerate(kda):
            if len(str(match['players'][i][stat])) == 2:
                kda_values[number] = str(match['players'][i][stat])
            else:
                kda_values[number] = '&{}&'.format(str(match['players'][i][stat]))
        kda_values.insert(1, '-')
        kda_values.insert(3, '-')
        kda_values = ''.join(kda_values)
        symbols = list(kda_values)
        kda_array = []
        for q, element in enumerate(symbols):
            array2.insert(2+q, cv2.imread('images/numbers/{}.png'.format(element)))
        #array2.insert(10, cv2.imread('images/vertical.png'))
        array2.append(cv2.imread('images/vertical.png'))
        array2.insert(0, cv2.imread('images/vertical.png'))

        try:
            array3.append(np.hstack(array2))
            array3.append(cv2.imread('images/448.png'))

        except:
            pass
        #cv2.imwrite('images/heroes/lineup/itemlist{}.png'.format(i), whole_items)
    array3.insert(0, cv2.imread('images/448.png'))
    pic2 = np.vstack(array3)
    pic3 = np.vstack([pic1, pic2])
    cv2.imwrite('images/heroes/lineup/itemlist2.png', pic3)


# not used
def winrate_solo(player_id):


    custom_args = {
                'players.account_id': player_id}
    custom_args.update(match_search_args)
    cursor = db['matches_all'].find(custom_args)
    cursor.sort('start_time', -1)
    hist = list(cursor)

    array2 = [0]*5
    array3 = [0]*5
    for game in hist:
        k = 0
        m = 0
        for j in range(10):
            try:
                if game['players'][j]['account_id'] in array_of_ids:
                    k += 1

                if game['players'][j]['account_id'] == player_id:
                    if game['radiant_win'] and j < 5 or (
                            not game['radiant_win'] and j > 4):

                            m += 1
            except:
                pass
        array2[k-1] += 1
        if m != 0:
            array3[k-1] += 1
    array = [0]*5
    print(array2)
    print(array3)
    for i in range(5):
        try:
            array[i] = round(array3[i]/array2[i], 2)
        except ZeroDivisionError:
            array[i] = 0
    return array


def all_time_records(player_id, *hero_id):
    if not hero_id:
        custom_args = {
                    'players.account_id': player_id}
    else:
        custom_args = {
                'players':
                {'$elemMatch': {"account_id": player_id, "hero_id": hero_id[0]}},
                }

    custom_args.update(match_search_args)
    cursor = db['matches_all'].find(custom_args)
    cursor.sort('start_time', -1)
    hist = list(cursor)
    array2 = [[0 for x in range(3)] for y in range(11)]
    array_stat = ['kills',
                  'deaths',
                  'assists',
                  'last_hits',
                  'denies',
                  'gold_per_min',
                  'xp_per_min',
                  'hero_damage',
                  'tower_damage',
                  'hero_healing',
                  'duration' # 10
                  ]

    for game in hist:
        match = game

        for i in range(10):
            try:
                if player_id == match['players'][i]['account_id']:
                    player_index = i
            except:
                pass
        x = match['players'][player_index]
        for i in range(10):
            try:    # old matches sometimes dont have all stats
                if x[array_stat[i]] > array2[i][0]:
                    array2[i][0] = x[array_stat[i]]
                    array2[i][1] = x['hero_id']
                    array2[i][2] = match['start_time']
            except:
                pass
        if match['duration'] > array2[10][0]:
            array2[10][0] = match['duration']
            array2[10][1] = match['players'][player_index]['hero_id']
            array2[10][2] = match['start_time']
    m, s = divmod(array2[10][0], 60)
    array2[10][0] = '{}m{}s'.format(m, s)
    reply = """{0}
            **All-Time Records{34}**:

**Kills**:          **{1}** {12} {23}
**Deaths**:         **{2}** {13} {24}
**Assists**:        **{3}** {14} {25}
**Lasthits**:       **{4}** {15} {26}
**Denies**:         **{5}** {16} {27}
**GPM**:            **{6}** {17} {28}
**XPM**:            **{7}** {18} {29}
**Hero Damage**:    **{8}** {19} {30}
**Tower Damage**:   **{9}** {20} {31}
**Hero Healing**:   **{10}** {21} {32}
**Longest Match**:  **{11}** {22} {33}
            """
    if not hero_id:
        return reply.format(
                    dic_reverse[player_id],
                    *[i[0] for i in array2],
                    *[' as **{}**'.format(hero_dic[i[1]]) if i[1] != 0 else "" for i in array2],
                    *['{} ago'.format(time_diff(i[2])) if i[2] != 0 else "" for i in array2],
                    ''
                )
    else:
        return reply.format(
                    dic_reverse[player_id],
                    *[i[0] for i in array2],
                    *['' for i in array2],
                    *['({} ago)'.format(time_diff(i[2])) if i[2] != 0 else "" for i in array2],
                    ' as {}'.format(hero_dic[hero_id[0]])
                )
