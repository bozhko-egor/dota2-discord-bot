from parser import Parser
from token_and_api_key import *
from hero_dictionary import hero_dic
from DotaDatabase import DotaDatabase
db = DotaDatabase('dota2-db')
db.connect()

k = 0
ids_to_parse = []

hero_ids = hero_dic.keys()
for player_id in ids_to_parse:
    for j in hero_ids:
        match_ids = []
        while True:
            try:
                data = Parser.get_match_history(player_id, hero_id=j)
            except:
                continue
            else:
                break
        while True:
            for i in range(len(data['matches'])):
                match_ids.append(data['matches'][i]['match_id'])
            if data['results_remaining'] == 0:
                break
            new_id = match_ids[-1]-1
            while True:
                try:
                    data = Parser.get_match_history(
                                player_id,
                                start_at_match_id=new_id,
                                hero_id=j
                                )
                except:
                    continue
                else:
                    break

        for i in match_ids:
            cursor = db.get_match_stat(i)
            if not cursor:
                while True:
                    try:
                        match = Parser.get_match_details(i)
                    except:
                        continue
                    else:
                        break

                db.add_match_stat(match)
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

                k += 1
                print("{}({})".format(k, j))
            else:
                print('match already in db!')



print('done!')
