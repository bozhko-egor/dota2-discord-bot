import requests
from .urls import BASE_URL, API_PATH

class ApiError(Exception):
    pass

class Api:

    def __init__(self):
        self.path = API_PATH[type(self).__name__]

    def _url(self, *subpath):
        if subpath:
            return BASE_URL + self.path + subpath[0]
        else:
            return BASE_URL + self.path

    def _get(self, url, **kwargs):

        response = requests.get(url, params=kwargs)

        if response.status_code == 200:
                return response.json()
        else:
            raise ApiError(str(response.status_code) + ': ' + response.url)
