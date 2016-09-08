from .api import Api


class Match(Api):
    '''match_id must be int'''

    def __init__(self, match_id):
        self.match_id = {'match_id': match_id}
        Api.__init__(self)
        self.path = self.path.format(**self.match_id)

    def info(self):
        url = self._url()
        return self._get(url)
