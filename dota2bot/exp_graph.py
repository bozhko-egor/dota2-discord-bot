from token_and_api_key import *
import pymongo
import numpy

import matplotlib.pyplot as pyplot

# in dire need of refactoring
conn = pymongo.MongoClient()
db = conn['dota-db']
player_id = 56232406
custom_args = {'result.players.account_id': player_id}
cursor = db['{}'.format(player_id)].find(custom_args)
cursor.sort('result.start_time', -1)
hist = list(cursor)
match = hist[0]['result']

level_dic = {
    1: 0,
    2:	200,
    3:	300,
    4:	400,
    5:	500,
    6:	600,
    7:	600,
    8: 	800,
    9:	1000,
    10:	1000,
    11:	600,
    12: 2200,
    13: 800,
    14: 1400,
    15: 1500,
    16:	1600,
    17:	1700,
    18:	1800,
    19:	1900,
    20: 2000,
    21: 2100,
    22: 2200,
    23:	2300,
    24:	2400,
    25:	2500
    }

exp_diff = numpy.zeros((250, 2))

k = -1
for i, player in enumerate(match['players']):
    for j in player["ability_upgrades"]:
        k += 1
        if i < 5:
            exp_diff[k][0] = level_dic[j['level']]
            exp_diff[k][1] = j['time']
        else:
            exp_diff[k][0] = -level_dic[j['level']]
            exp_diff[k][1] = j['time']

a = sorted(exp_diff, key=lambda x: x[1])
b = []
for i in a:
    if i[0] != 0:
        b.append(i)
for i, number in enumerate(b):
    if i > 0:
        b[i][0] += b[i-1][0]
time = []
exp = []
for i, number in enumerate(b):
    time.append(b[i][1])
    exp.append(b[i][0])
time1 = [(x-200) // 60 for x in time]
time2 = []
exp2 = []
for i, obj in enumerate(time1):
    if time1[i:].count(obj) == 1:
        time2.append(time1[i])
        exp2.append(exp[i])

x = time2
y = exp2

h = [0, 60]
t = [0, 0]
pyplot.plot(x, y)
pyplot.plot(h, t, label='$T_{7}(x)$')
pyplot.savefig('example01.png')
print(time2)
