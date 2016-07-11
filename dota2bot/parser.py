import json
from urllib.request import urlopen
from token_and_api_key import api_key
from urls import *


class Parser:
    # 100 results per api call
    def get_match_history(account_id, **kwargs):
        url = get_history_url
        for name, value in kwargs.items():
            url += "&{0}={1}".format(name, value)
        html = urlopen(url.format(account_id, api_key)).read()
        data = json.loads(html.decode('utf-8'))
        return data['result']

    def get_match_details(match_id):
        html = urlopen(get_match_url.format(match_id, api_key)).read()
        data = json.loads(html.decode('utf-8'))
        return data['result']

    #def get_winrate:

    #def get playernumber:

    #def get league listing

    #def get upcomnimg matches:
