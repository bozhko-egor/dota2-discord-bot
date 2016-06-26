import json
from urllib.request import urlopen
from token_and_api_key import *
import pymongo

conn = pymongo.MongoClient()
db = conn['dota-db']

k = 0
ids_to_parse = []

hero_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20,
            21, 22, 23, 25, 31, 26, 27, 28, 29, 30, 32, 33, 34, 35, 36, 37, 38, 39, 40,
            41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58,
            59, 60, 61, 62, 63, 64, 65, 66, 67, 69, 68, 70, 71, 72, 73, 74, 75, 76,
            77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94,
            95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 106, 107, 109, 110, 111,
            105, 112, 113]
for player_id in ids_to_parse:
    for j in hero_ids:
        match_ids = []
        while True:
            try:
                html = urlopen("https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?hero_id={}&account_id={}&key={}".format(j, player_id, api_key)).read()
            except:
                continue
            else:
                break
        while True:
            data = json.loads(html.decode('utf-8'))

            for i in range(len(data['result']['matches'])):
                match_ids.append(data['result']['matches'][i]['match_id'])
            if data['result']['results_remaining'] == 0:
                break
            new_id = match_ids[-1]-1
            while True:
                try:
                    html = urlopen("https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?start_at_match_id={}&hero_id={}&account_id={}&key={}".format(new_id, j, player_id, api_key)).read()
                except:
                    continue
                else:
                    break

        for i in match_ids:
            while True:
                try:
                    html2 = urlopen("https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?match_id={}&key={}".format(i, api_key)).read()
                except:
                    continue
                else:
                    break

            data2 = json.loads(html2.decode('utf-8'))

            db['{}'.format(player_id)].insert_one(data2)
            # cursor = db.games.find()
            k += 1
            print("{}({})".format(k, j))

print('done!')
