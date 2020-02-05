import requests
import weakref

from aiohttp.hdrs import USER_AGENT

from .const import (
    # _LOG,
    USER_AGENT_PRODUCT,
    USER_AGENT_PRODUCT_VERSION,
    USER_AGENT_SYSTEM_INFORMATION,
    # CLIENT_ID,
)

from .endpoints import (
    API_URL,
    AUTH_URL,
    APP_MUST_UPDATE,
    USER_CONFIG,
    USER_VERIFY_EMAIL,
    USER_LOGIN,
    DATA_LATEST,
)


class UHooAPI(object):
    def __init__(self, session=None):
        self._headers = {
            USER_AGENT: f"{USER_AGENT_PRODUCT}/{USER_AGENT_PRODUCT_VERSION} "
            + f"({USER_AGENT_SYSTEM_INFORMATION})"
        }

        if session is not None:
            session = weakref.ref(session)
        else:
            session = requests.session()

        self._session = session

    def app_must_update(self):
        url = f"{API_URL}{APP_MUST_UPDATE}"
        payload = {"version": "93"}

        response = self._session.post(url, data=payload, headers=self._headers)

        if response.ok:
            # need to look at response value
            # when app does not need to update response is '0'
            return True
        else:
            return False

    def user_config(self):
        url = f"{AUTH_URL}{USER_CONFIG}"

        response = self._session.get(url, headers=self._headers)

        response_json = None
        if response.ok:
            response_json = response.json()

        return response_json

    def user_verify_email(self, username, clientId):
        url = f"{AUTH_URL}{USER_VERIFY_EMAIL}"
        payload = {
            "username": username,
            "clientId": clientId,
        }

        response = self._session.post(url, data=payload, headers=self._headers)

        response_json = None
        if response.ok:
            response_json = response.json()

        return response_json

    def user_login(self, username, password, clientId):
        """Note: password is an encrypted hash of the user's password"""
        url = f"{AUTH_URL}{USER_LOGIN}"
        payload = {
            "username": username,
            "password": password,
            "clientId": clientId,
        }

        response = self._session.post(url, data=payload, headers=self._headers)

        response_json = None
        if response.ok:
            response_json = response.json()

        return response_json

    def data_latest(self):
        url = f"{API_URL}{DATA_LATEST}"

        response = self._session.get(url, headers=self._headers)

        response_json = None
        if response.ok:
            response_json = response.json()

        return response_json


# login_payload = {
#     'password': enc_password_hash,
#     'clientId': clientId,
#     'username': username
# }

# r = s.post(baseurl_auth + user_login,
#            data=login_payload,
#            headers=headers)

# print(r.status_code)
# print(r.headers)
# print(r.text)

# token = ''
# refreshToken = ''
# if (r.status_code == 200):
#     r_json = r.json()
#     if ('token' in r_json):
#         token = r_json['token']
#     if ('refreshToken' in r_json):
#         refreshToken = r_json['refreshToken']

# headers['Authorization'] = 'Bearer {}'.format(refreshToken)

# {
#   "token": "",
#   "refreshToken": "",
#   "deviceId": "",
#   "name": "",
#   "lastname": "",
#   "Role": "mobile users",
#   "status": 1,
#   "gdpr": 1,
#   "language": {
#     "code": "en",
#     "name": "English"
#   },
#   "Roletype": null,
#   "companyName": null,
#   "clientName": null
# }
