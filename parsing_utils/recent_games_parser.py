from token_and_api_key import *
from .parser import Parser
from cogs.utils.resources import db



def get_recent_matches(player_id):
    p = 0

    args = {'players.account_id': player_id}

    hist = db.get_match_list(args)

    match_ids = []

    data = Parser.get_match_history(player_id)

    if data:
        k = 0
        while True:
            try:
                if hist[0]['match_id'] != data['matches'][k]['match_id']:
                    match_ids.append(data['matches'][k]['match_id'])
                    print("{}".format(k))
                    k += 1
            except IndexError:
                return
            else:
                if hist[1]['match_id'] != data['matches'][k+1]['match_id']:
                    match_ids.append(data['matches'][k]['match_id'])  # rare ocassion of missing matches in db
                break
    else:
        return "Dota 2 api is down"
    if len(match_ids) != 0:
        for i in match_ids:
            match = Parser.get_match_details(i)
            if match:
                db.add_match_stat(match)

                dota_ids = []
                for j in range(10):
                    dota_ids.append(match['players'][j]['account_id'])

                steam_arr = Parser.get_steam_info(dota_ids)

                for j in range(10):

                    player = match['players'][j]

                    steam_name = 0
                    for _, entry in enumerate(steam_arr):
                        if player['account_id'] + 76561197960265728 == int(entry['steamid']):
                            steam_name = entry['personaname']
                    if not steam_name:
                        steam_name = "Unknown"
                    db.update_name(steam_name, match['match_id'], player['account_id'])

                p += 1
            else:
                return "Dota 2 api is down"
    else:
        print('No new matches to parse')
    return p

if __name__ == '__main__':
    print(get_recent_matches())
