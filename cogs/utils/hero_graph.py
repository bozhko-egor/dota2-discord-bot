import math
import matplotlib.pyplot as plt
from .hero_dictionary import hero_dic
import matplotlib.dates as mdates
from opendota_api.player import Player

def hero_per_month(player_id, hero_id):
    hist = Player(player_id).stat_func('matches', hero_id=hero_id)
    hist = hist[::-1]
    time = hist[0]['start_time']
    quantity = []
    kk = 0
    m = 0
    q = 0
    month = []
    for i in hist:

        if i['start_time'] < time:

            try:
                if i['hero_id'] == hero_id:
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
