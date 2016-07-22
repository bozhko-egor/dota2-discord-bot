import pymongo
import math
import matplotlib.pyplot as plt
from .hero_dictionary import hero_dic
import matplotlib.dates as mdates
conn = pymongo.MongoClient()
db = conn['dota2-db']


def hero_per_month(player_id, hero_id):
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
            for j in range(10):
                try:
                    if i['players'][j]['account_id'] == player_id:

                        if i['players'][j]['hero_id'] == hero_id:
                            q += 1
                            kk += 1
                except:
                        pass
        else:
            time += 2592000
            quantity.append(q)
            month.append(time)
            q = 0
            m += 1

    plt.xkcd()
    plt.gca().cla()

    plt.title('number of games played as {} per month'.format(hero_dic[hero_id]))

    y = quantity

    secs = mdates.epoch2num(month)

    ax = plt.gca()

    years = mdates.YearLocator()   # every year
    yearsFmt = mdates.DateFormatter('%Y')

    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    tick = 5 if max(y) > 20 else 1
    yint = range(min(y), math.ceil(max(y))+2, tick)  # set only int ticks
    plt.yticks(yint)
    plt.plot(secs, y, color='blue')

    plt.savefig('images/graphs/hero.png')

    return "{} games".format(kk)
