from token_and_api_key import *
import pymongo
from stat_func import big_pic
from random import randint
from random import shuffle
from stat_func import match_search_args
from hero_dictionary import hero_dic
import pickle

conn = pymongo.MongoClient()
db = conn['dota2-db']

def guessing_game():
    global match_search_args
    player_id = array_of_ids[randint(0, len(array_of_ids)-1)]
    custom_args = {
                'players.account_id': player_id}
    custom_args.update(match_search_args)
    cursor = db['matches_all'].find(custom_args)
    cursor.sort('start_time', -1)
    hist = list(cursor)
    match_number = randint(0, len(hist)-1)
    match = hist[match_number]
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
    hero_id = hist[match_number]['players'][player_index]['hero_id']
    hero = hero_dic[hero_id]
    big_pic(match_number, player_id)
    return [hero, dic_reverse[player_id], game_status]

def roulette(n, dosh, player_id):
    roll = randint(0, 100)
    if 0 <= roll <= 66:
        reply = "You lost {}$".format(n)
        dosh[player_id] -= n
        with open('dosh.pickle', 'wb') as f:
                pickle.dump(dosh, f)
    elif 67 <= roll <= 94:
        reply = "You won {}$".format(2*n)
        dosh[player_id] += n
        with open('dosh.pickle', 'wb') as f:
                pickle.dump(dosh, f)
    elif 96 <= roll <= 99:
        reply = "You won {}$".format(4*n)
        dosh[player_id] += 3*n
        with open('dosh.pickle', 'wb') as f:
                pickle.dump(dosh, f)
    elif roll == 100:
        reply = "You won {}$".format(10*n)
        dosh[player_id] += 9*n
        with open('dosh.pickle', 'wb') as f:
                pickle.dump(dosh, f)
    return reply
