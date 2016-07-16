import json
from urllib.request import urlopen
from token_and_api_key import api_key
from urls import *
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

    #def get playernumber:

    #def get league listing

    #def get upcomnimg matches:
