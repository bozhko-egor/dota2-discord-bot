import json
from urllib.request import urlopen
from token_and_api_key import *
import pymongo


conn = pymongo.MongoClient()
db = conn['dota-db']


def get_recent_matches(player_id):
    p = 0

    custom_args = {'result.players.account_id': player_id}
    cursor = db['{}'.format(player_id)].find(custom_args)
    cursor.sort('result.start_time', -1)
    hist = list(cursor)
    match_ids = []
    n_of_tries = 0
    while True:
        try:
            html = urlopen("https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?account_id={}&key={}".format(player_id, api_key)).read()
        except:
            continue
            n_of_tries += 1
        if n_of_tries > 50:
            return("Dota 2 api is down")
            break
        else:
            break
    data = json.loads(html.decode('utf-8'))
    k = 0
    while True:
        if hist[0]['result']['match_id'] != data['result']['matches'][k]['match_id']:
            match_ids.append(data['result']['matches'][k]['match_id'])
            print("{}".format(k))
            k += 1
        else:
            break
    if len(match_ids) != 0:
        for i in match_ids:
            while True:
                try:
                    html2 = urlopen("https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?match_id={}&key={}".format(i, api_key)).read()
                except:
                    continue
                    n_of_tries += 1
                    if n_of_tries > 50:
                        return("Dota 2 api is down")
                        break
                else:
                    break

            data2 = json.loads(html2.decode('utf-8'))
            db['{}'.format(player_id)].insert_one(data2)
            p += 1
    else:
        print('No new matches to parse')

    return "{} - {} games".format(dic_reverse[player_id], p)

#if __name__ == '__main__':
#    get_recent_matches()
