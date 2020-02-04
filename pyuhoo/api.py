import requests
import weakref

from .const import (
    # _LOG,
    # API_URL,
    # AUTH_URL,
    USER_AGENT_PRODUCT,
    USER_AGENT_PRODUCT_VERSION,
    USER_AGENT_SYSTEM_INFORMATION,
)


class UHooAPI(object):
    def __init__(self, session=None):
        self._headers = {
            "User-Agent": "{0}/{1} ({2})".format(
                USER_AGENT_PRODUCT,
                USER_AGENT_PRODUCT_VERSION,
                USER_AGENT_SYSTEM_INFORMATION,
            )
        }

        if session is not None:
            session = weakref.ref(session)
        else:
            session = requests.session()

        self._session = session

    def app_must_update(self):
        pass
