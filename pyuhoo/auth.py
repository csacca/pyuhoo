import weakref
import requests.auth

# from .const import (
#     _LOG,
#     API_URL,
#     AUTH_URL,
# )


class UHooAuth(requests.auth.AuthBase):
    def __init__(self, session=None):
        if session is not None:
            session = weakref.ref(session)
        self._session = session

    def login(self, headers=None):
        pass
