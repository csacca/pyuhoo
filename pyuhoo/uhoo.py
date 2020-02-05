from .api import API


class uHoo(object):
    def __init__(self):
        self._api = API()
        self._auth_token = None

    def login(self):
        pass
