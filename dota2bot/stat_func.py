import pymongo
import cv2
import numpy as np
from hero_dictionary import game_mode_dic
from hero_dictionary import hero_dic
from hero_dictionary import item_dic

conn = pymongo.MongoClient()
db = conn['dota-db']

match_search_args = {
            'result.game_mode': {'$in': [0, 1, 2, 3, 4, 5, 12, 14, 16, 22]},
            'result.duration': {'$gt': 720},
            'result.players.level': {'$nin': [1, 2, 3]},
            'result.players.leaver_status': {'$nin': [5, 6]},
            'result.lobby_type': {'$in': [0, 5, 6, 7]}
            }


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
        for i, game in enumerate(hist):
            for j in range(10):
                if game['result']['players'][j]['account_id'] == player_id1:
                    if game['result']['radiant_win'] and j < 5 or (
                            not game['result']['radiant_win'] and j > 4):
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

    for i, game in enumerate(hist):
        for j in range(10):
            try:
                if game['result']['players'][j]['account_id'] == player_id1:
                    if game['result']['radiant_win'] and j < 5 or (
                            not game['result']['radiant_win'] and j > 4):
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
    for i, game in enumerate(hist):
        for j in range(10):
            if game['result']['players'][j]['account_id'] == player_id:
                if game['result']['radiant_win'] and j < 5 or (
                        not game['result']['radiant_win'] and j > 4):
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
        played on {date} ({time_passed}), {game_status}""".format(**stats)
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
            'result.players':
            {'$elemMatch': {"account_id": player_id, "hero_id": hero_id}},
            }
    custom_args.update(match_search_args)
    cursor = db['{}'.format(player_id)].find(custom_args)
    hist = list(cursor)
    k = 0

    for m, game in enumerate(hist):
        match = game['result']
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

        array2.insert(0, cv2.imread(
            'images/heroes/{} icon.png'.format(hero_dic[
                match['players'][i]['hero_id']].lower()), 1))
        array2.insert(1, cv2.imread('images/vertical.png'))
        array2.insert(-1, cv2.imread('images/vertical.png'))
        array2.insert(0, cv2.imread('images/vertical.png'))
        try:
            array3.append(np.hstack(array2))
            array3.append(cv2.imread('images/346.png'))

        except:
            pass

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

        array2.insert(0, cv2.imread(
            'images/heroes/{} icon.png'.format(hero_dic[
                match['players'][i]['hero_id']].lower()), 1))
        array2.insert(1, cv2.imread('images/vertical.png'))
        array2.append(cv2.imread('images/vertical.png'))
        array2.insert(0, cv2.imread('images/vertical.png'))
        try:
            array3.append(np.hstack(array2))
            array3.append(cv2.imread('images/302.png'))

        except:
            pass

    array3.insert(0, cv2.imread('images/302.png'))
    pic2 = np.vstack(array3)
    pic3 = np.hstack([pic1, pic2])
    cv2.imwrite('images/heroes/lineup/itemlist2.png', pic3)
