import json
from urllib.request import urlopen
import urllib



def get_upcoming_matches(*league_ids):
    get_upcoming_games = "http://dailydota2.com/match-api"
    html = urlopen(get_upcoming_games).read()
    data = json.loads(html.decode('utf-8'))
    upcoming_matches = []
    if league_ids:
        for game in data['matches']:
            if int(game['league']['league_id']) in league_ids:
                upcoming_matches.append(game)
        return upcoming_matches
    else:
        return data['matches']

def get_top_streams(game_name):
    url = "https://api.twitch.tv/kraken/streams?game="

    url += game_name.replace(' ', '+')
    html = urlopen(url).read()
    streams = json.loads(html.decode('utf-8'))['streams']

    template = "{5} streams:\n\n**1.** {0}\n\n**2.** {1}\n\n**3.** {2}\n\n**4.** {3}\n\n**5.** {4}"
    message = "{} ({}viewers) `{}`"
    entries = []
    for i in range(5):
        msg_new = message.format(
            streams[i]['channel']['status'].replace('`', "'"),
            streams[i]['viewers'],
            streams[i]['channel']['url']
            )
        entries.append(msg_new)
    template = template.format(*entries, game_name.capitalize())
    return template
