from .parser import Parser
from token_and_api_key import *
from cogs.utils.hero_dictionary import hero_dic
from cogs.utils.resources import db


def history_parser(player_id, hero_id):
    while True:
        try:
            k = 0
            new_matches = 0
            match_ids = []

            data = Parser.get_match_history(player_id, hero_id=hero_id)

            while True:
                for i in range(len(data['matches'])):
                    match_ids.append(data['matches'][i]['match_id'])
                if data['results_remaining'] == 0:
                    break
                new_id = match_ids[-1]-1

                data = Parser.get_match_history(
                            player_id,
                            start_at_match_id=new_id,
                            hero_id=hero_id
                            )

            for i in match_ids:
                cursor = db.get_match_stat(i)  # если матча нет в дб
                if not cursor:

                    match = Parser.get_match_details(i)


                    db.add_match_stat(match)
                    new_matches += 1
                    dota_ids = []
                    for q in range(10):
                        dota_ids.append(match['players'][q]['account_id'])

                    steam_arr = Parser.get_steam_info(dota_ids)

                    for q in range(10):

                        player = match['players'][q]

                        steam_name = 0
                        for _, entry in enumerate(steam_arr):
                            if player['account_id'] + 76561197960265728 == int(entry['steamid']):
                                steam_name = entry['personaname']
                        if not steam_name:
                            steam_name = "Unknown"
                        db.update_name(steam_name, match['match_id'], player['account_id'])
        except (TypeError, IndexError):
            k += 1
            if k > 5:
                return
            continue

        else:
            break
    return new_matches
