import weakref

import requests

from aiohttp.hdrs import AUTHORIZATION, USER_AGENT

from .const import (
    _LOG,
    USER_AGENT_PRODUCT,
    USER_AGENT_PRODUCT_VERSION,
    USER_AGENT_SYSTEM_INFORMATION,
)
from .endpoints import (
    API_URL,
    APP_MUST_UPDATE,
    AUTH_URL,
    DATA_HOUR,
    DATA_LATEST,
    DEVICE_DATA,
    USER_CONFIG,
    USER_LOGIN,
    USER_VERIFY_EMAIL,
)


class APIError(Exception):
    def __init__(self, response, msg=None):
        if response is None:
            response_content = b""
        else:
            try:
                response_content = response.content
            except AttributeError:
                response_content = response.data

        if response_content != b"":
            if isinstance(response, requests.Response):
                message = response.json()["error"]
        else:
            message = "API Error Occured"

        if msg is not None:
            message = "API Error Occured: " + msg

        super(APIError, self).__init__(message)

        self.response = response


class API(object):
    def __init__(self, session=None):
        self._user_agent = (
            f"{USER_AGENT_PRODUCT}"
            + "/"
            + f"{USER_AGENT_PRODUCT_VERSION} "
            + f"({USER_AGENT_SYSTEM_INFORMATION})"
        )

        if session is not None:
            session = weakref.ref(session)
        else:
            session = requests.session()

        self._session = session

        self._session.headers.update({USER_AGENT: self._user_agent})

    def _request(self, method, url, payload=None):
        _LOG.debug(f"<- {method} {url}")
        response = self._session.request(method, url, data=payload)
        _LOG.debug(f"-> {response.status_code}")

        if not response.ok:
            raise APIError(response, f"Recieved status code {response.status_code}")
        return response.json()

    def _get(self, url):
        return self._request("GET", url)

    def _post(self, url, payload=None):
        return self._request("POST", url, payload)

    def set_auth_token(self, token):
        self._session.headers.update({AUTHORIZATION: f"Bearer {token}"})

    def app_must_update(self, version):
        url = f"{API_URL}{APP_MUST_UPDATE}"
        payload = {"version": version}

        response = self._post(url, payload)

        if response == 0:
            return False
        else:
            _LOG.debug(f"[app_must_update] recieved non-zero response: {response}")
            return True

    def user_config(self):
        url = f"{AUTH_URL}{USER_CONFIG}"

        response = self._get(url)
        return response

    def user_verify_email(self, username, client_id):
        url = f"{AUTH_URL}{USER_VERIFY_EMAIL}"
        payload = {
            "username": username,
            "clientId": client_id,
        }

        response = self._post(url, payload)
        return response

    def user_login(self, username, password, client_id):
        """Note: password is an encrypted hash of the user's password"""
        url = f"{AUTH_URL}{USER_LOGIN}"
        payload = {
            "username": username,
            "password": password,
            "clientId": client_id,
        }

        response = self._post(url, payload)
        return response

    def data_latest(self):
        url = f"{API_URL}{DATA_LATEST}"

        response = self._get(url)
        return response

    def data_hour(self, serial_number, prev_date_time):
        url = f"{API_URL}{DATA_HOUR}"
        payload = {
            "serialNumber": serial_number,
            "prevDateTime": prev_date_time,
        }

        response = self._post(url, payload)
        return response

    def device_data(self, serial_number):
        url = f"{API_URL}{DEVICE_DATA}"
        payload = {
            "serialNumber": serial_number,
        }

        response = self._post(url, payload)
        return response
