from .api import Api
from .urls import PLAYER_PATH


class Player(Api):
    '''account_id : int'''
    def __init__(self, account_id):
        self.account_id = {'account_id': account_id}
        Api.__init__(self)
        self.path = self.path.format(**self.account_id)

    def info(self):
        '''Returns player's account data'''
        url = self._url()
        return self._get(url)

    def stat_func(self, stat, **kwargs):
        """Stat list:
        'wl' - Returns a Dota 2 player's wins/losses,
        'matches' - Returns list of player's Dota 2 matches,
        'heroes' - Returns list of dictionaries with data about heroes played,
        'peers' - Returns player data,
        'activity' -
        'records'
        'counts'
        'wardmap'
        'items'
        'wordcloud'
        'ratings'
        'rankings'
        'histograms'
        'trends'"""
        url = self._url(PLAYER_PATH[stat])
        return self._get(url, **kwargs)
