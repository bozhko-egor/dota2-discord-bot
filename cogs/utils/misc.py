from token_and_api_key import *
from random import randint
from random import shuffle
from .hero_dictionary import hero_dic
from .resources import db
from .post_game_screen import post_game_guess
from opendota_api.matches import Match
from opendota_api.player import Player

def guessing_game(server, ctx):
    ids = db.get_all_ids_on_server(server)
    player_id = ids[randint(0, len(ids)-1)]
    hist = Player(player_id).stat_func('matches')
    match_number = randint(0, len(hist)-1)
    match_id = hist[match_number]['match_id']
    match = Match(match_id).info()
    array3 = []
    game_type = "Solo."
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

    shuffle(array3)
    if (player_index > 4 and match['radiant_win']) or (
        player_index < 5 and not match['radiant_win']
    ):
        game_status = game_type + ", ".join(array3)
    elif (player_index > 4 and not match['radiant_win']) or (
          player_index < 5 and match['radiant_win']
    ):
        game_status = game_type + ", ".join(array3)
    hero_id = match['players'][player_index]['hero_id']
    hero = hero_dic[hero_id]

    discord_id_1 = db.get_discord_id(player_id, ctx.message.server.id)
    for member in ctx.message.server.members:
        if discord_id_1 == member.id:
            name = member.name
    post_game_guess(match)

    return [hero, name, game_status]
