import json
from urllib.request import urlopen
from token_and_api_key import api_key
from .urls import *
import urllib


class Parser:
    # 100 results per api call
    def get_match_history(account_id, **kwargs):
        url = get_history_url
        for name, value in kwargs.items():
            url += "&{0}={1}".format(name, value)
        try:
            html = urlopen(url.format(account_id, api_key)).read()
        except urllib.error.HTTPError:
            return
        data = json.loads(html.decode('utf-8'))
        return data['result']

    def get_match_details(match_id):
        try:
            html = urlopen(get_match_url.format(match_id, api_key)).read()
        except urllib.HTTPError:
            return
        data = json.loads(html.decode('utf-8'))
        return data['result']

    def get_league_list(*league_ids):
        html = urlopen(get_leagues.format(api_key)).read()
        data = json.loads(html.decode('utf-8'))
        leagues = []
        if league_ids:
            for league in data['result']['leagues']:
                if league['leagueid'] in league_ids:
                    leagues.append(league)
            return leagues
        else:
            return data['result']

    def get_live_games(league_id):
            html = urlopen(get_games.format(api_key)).read()
            data = json.loads(html.decode('utf-8'))
            matches = []
            for game in data['result']['games']:
                if game['league_id'] == league_id:
                    matches.append(game)
            return matches

    def get_teams_info(**kwargs):  # (teams_requested, start_at_team_id)
        url = get_team_list
        for name, value in kwargs.items():
            url += "&{0}={1}".format(name, value)
        html = urlopen(url.format(api_key)).read()
        data = json.loads(html.decode('utf-8'))
        return data['result']['teams']

    def get_upcoming_matches(*league_ids):
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

    def get_steam_info(account_ids):

        account_ids = [x + 76561197960265728 for x in account_ids]
        url = get_account_info
        for ID in account_ids:
            url += '{},'.format(str(ID))
        html = urlopen(url.format(api_key)).read()
        data = json.loads(html.decode('utf-8'))
        return data['response']['players']


    def get_steam_nickname(account_ids):
        data = Parser.get_steam_info(account_ids)
        if data:
            return data[0]['personaname']
        else:
            return "Unknown"

    def get_top_streams(game_name):
        url = get_top_twitch_streams

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
    #def get playernumber:

    #def get league listing

    #def get upcomnimg matches:
