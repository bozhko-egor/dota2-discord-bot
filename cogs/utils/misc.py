from token_and_api_key import *
from random import randint
from random import shuffle
from .hero_dictionary import hero_dic
from .resources import db
from .post_game_screen import post_game_guess

def guessing_game(server):
    ids = db.get_all_ids_on_server(server)
    player_id = ids[randint(0, len(ids)-1)]
    args = {
                'players.account_id': player_id}
    hist = db.get_match_list(args)
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
        game_status = game_type + ", ".join(array3)
    elif (player_index > 4 and not match['radiant_win']) or (
          player_index < 5 and match['radiant_win']
    ):
        game_status = game_type + ", ".join(array3)
    hero_id = hist[match_number]['players'][player_index]['hero_id']
    hero = hero_dic[hero_id]
    post_game_guess(match)
    return [hero, dic_reverse[player_id], game_status]
