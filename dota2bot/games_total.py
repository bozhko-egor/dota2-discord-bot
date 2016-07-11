import pymongo

import matplotlib.pyplot as plt
from matplotlib import pylab
from hero_dictionary import hero_dic

conn = pymongo.MongoClient()
db = conn['dota2-db']
def total(player_id):
    match_search_args = {
                'game_mode': {'$in': [0, 1, 2, 3, 4, 5, 12, 14, 16, 22]},
                'duration': {'$gt': 720},
                'players.level': {'$nin': [1, 2, 3]},
                'players.leaver_status': {'$nin': [5, 6]},
                'lobby_type': {'$in': [0, 5, 6, 7]}
                }

    custom_args = {
                'players.account_id': player_id}
    custom_args.update(match_search_args)
    cursor = db['matches_all'].find(custom_args)
    cursor.sort('start_time', 1)
    hist = list(cursor)
    time = hist[0]['start_time']

    quantity = []
    kk = 0
    m = 0
    q = 0
    month = []
    for i in hist:

        if i['start_time'] < time:

                            q += 1
                            kk += 1

        else:
            time += 2592000
            quantity.append(q)
            month.append(time)
            q = 0
            m += 1

    plt.figure()
    plt.xkcd()

    plt.title('number of games played per month')

    x = month
    y = quantity
    frame = pylab.gca()

    frame.axes.get_xaxis().set_ticks([])

    plt.plot(x, y)

    plt.savefig('images/graphs/total.png')

    return "{} games".format(kk)
total()
