import json
from urllib.request import urlopen
from token_and_api_key import *
import pymongo
import pickle

conn = pymongo.MongoClient()
db = conn['dota-db']


p = 0
for player_id in array_of_ids:
    custom_args = {'result.players.account_id': player_id}
    cursor = db['{}'.format(player_id)].find(custom_args)
    cursor.sort('result.start_time', -1)
    hist = list(cursor)
    match_ids = []
    while True:
        try:
            html = urlopen("https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?account_id={}&key={}".format(player_id, api_key)).read()
        except:
            continue
        else:
            break
    data = json.loads(html.decode('utf-8'))
    k = 0
    while True:
        if hist[0]['result']['match_id'] != data['result']['matches'][k]['match_id']:
            match_ids.append(data['result']['matches'][k]['match_id'])
            print("{}k".format(k))
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
                else:
                    break
            data2 = json.loads(html2.decode('utf-8'))
            with open('dosh.pickle', 'rb') as f:
                dosh = pickle.load(f)
            for j in range(10):
                if data2['result']['players'][j]['account_id'] == player_id:
                    if data2['result']['radiant_win'] and j < 5 or (
                            not data2['result']['radiant_win'] and j > 4):

                            dosh[dic_reverse[player_id]] += 25
                    else:
                        dosh[dic_reverse[player_id]] -= 25
            with open('dosh.pickle', 'wb') as f:
                pickle.dump(dosh, f)
            db['{}'.format(player_id)].insert_one(data2)
            p += 1
            print(p)
    else:
        print('no new matches to parse')
print('done!')
