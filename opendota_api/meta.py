from .api import Api


class Metadata(Api):

    def metadata(self):
        url = self._url()
        return self._get(url)


class Distributions(Api):

    def distr(self):
        url = self._url()
        return self._get(url)


class Search(Api):
    """takes only one arg"""
    def search(self, query):
        url = self._url()
        return self._get(url, q=query)


class Rankings(Api):

    def rank(self, hero_id):
        url = self._url()
        return self._get(url, hero_id=str(hero_id))

class Benchmarks(Api):

    def benchmarks(self, hero_id):
        url = self._url()
        return self._get(url, hero_id=str(hero_id))
