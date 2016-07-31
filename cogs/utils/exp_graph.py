import numpy as np
import matplotlib.pyplot as plt
from .resources import db

player_id = 56232406
args = {'match_id': 2356515163}

hist = db.get_match_list(args)
match = hist[0]

level_dic = {
    1:  0,
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

exp_diff = np.zeros((250, 2))

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
time2.insert(0, 0)
exp2.insert(0, 0)
x = time2

# neg_exp = [0 if i >= 0 else i for i in exp2]
# pos_exp = [0 if i <= 0 else i for i in exp2]

print(pos_exp, neg_exp, time)
plt.xkcd()

# style.use('seaborn-poster')

plt.title('Exp difference')


plt.plot(x, exp2, color='blue')

plt.axhline(0, color='black')
plt.savefig('images/graphs/example01.png')

print(max(exp2), min(exp2))
