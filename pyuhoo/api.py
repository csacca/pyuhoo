import logging
from typing import Optional, Union

from aiohttp import ClientError, ClientResponseError, ClientSession
from aiohttp.hdrs import AUTHORIZATION, USER_AGENT

from .consts import (
    USER_AGENT_PRODUCT,
    USER_AGENT_PRODUCT_VERSION,
    USER_AGENT_SYSTEM_INFORMATION,
)
from .endpoints import (
    API_URL_SCAFFOLD,
    APP_MUST_UPDATE,
    AUTH_URL_SCAFFOLD,
    DATA_HOUR,
    DATA_LATEST,
    DEVICE_DATA,
    USER_CONFIG,
    USER_LOGIN,
    USER_REFRESH_TOKEN,
    USER_VERIFY_EMAIL,
)
from .errors import ForbiddenError, RequestError, UnauthorizedError
from .util import json_pp


class API(object):
    """uHoo API"""

    def __init__(self, websession: ClientSession) -> None:
        self._log: logging.Logger = logging.getLogger("pyuhoo")

        self._user_agent: str = (
            f"{USER_AGENT_PRODUCT}"
            + "/"
            + f"{USER_AGENT_PRODUCT_VERSION} "
            + f"({USER_AGENT_SYSTEM_INFORMATION})"
        )

        self._websession: ClientSession = websession

        self._bearer_token: Optional[str] = None

    async def _request(
        self, method: str, scaffold: str, endpoint: str, data: Optional[dict] = None
    ):
        headers = {}
        if self._bearer_token:
            headers.update({AUTHORIZATION: f"Bearer {self._bearer_token}"})
        if self._user_agent:
            headers.update({USER_AGENT: self._user_agent})

        self._log.debug(f"[_request] {method} {scaffold}/{endpoint}")

        if method.lower() == "post":
            self._log.debug(f"[_request] {json_pp(data)}")

        async with self._websession.request(
            method, f"{scaffold}/{endpoint}", headers=headers, data=data
        ) as resp:
            try:
                self._log.debug(
                    f"[_request] {resp.status} {method} {scaffold}/{endpoint}"
                )

                if resp.content_type == "application/json":
                    json = await resp.json()
                else:
                    text = await resp.text()

                resp.raise_for_status()

                return json

            except ClientResponseError as err:
                if err.status == 401:
                    self._log.debug(f"[_request] 401 Unauthorized:\n{json_pp(json)}")
                    raise UnauthorizedError() from None
                elif err.status == 403:
                    self._log.debug(f"[_request] 403 Unauthorized:\n{text}")
                    raise ForbiddenError() from None
                else:
                    raise RequestError(
                        f"Error requesting data from {scaffold}/{endpoint}: {err}"
                    ) from None

            except ClientError as err:
                raise RequestError(
                    f"Error requesting data from {scaffold}/{endpoint}: {err}"
                ) from None

    def set_bearer_token(self, bearer_token: Optional[str]) -> None:
        self._bearer_token = bearer_token

    async def app_must_update(self, version: int) -> bool:
        resp: Union[int, dict] = await self._request(
            "post", API_URL_SCAFFOLD, APP_MUST_UPDATE, data={"version": version}
        )
        if resp == 0:
            return False
        else:
            self._log.debug(f"[app_must_update] received non-zero response: {resp}")
            return True

    async def user_config(self) -> dict:
        resp: dict = await self._request("get", AUTH_URL_SCAFFOLD, USER_CONFIG)
        return resp

    async def user_verify_email(self, username: str, client_id: str) -> dict:
        resp: dict = await self._request(
            "post",
            AUTH_URL_SCAFFOLD,
            USER_VERIFY_EMAIL,
            data={"username": username, "clientId": client_id},
        )
        return resp

    async def user_login(self, username: str, password: str, client_id: str) -> dict:
        """Note: password is an encrypted hash of the user's password"""
        resp: dict = await self._request(
            "post",
            AUTH_URL_SCAFFOLD,
            USER_LOGIN,
            data={"username": username, "password": password, "clientId": client_id},
        )
        return resp

    async def user_refresh_token(self, token, user_device_id) -> dict:
        """Note: user_device_id is the same as client_id"""
        resp: dict = await self._request(
            "post",
            AUTH_URL_SCAFFOLD,
            USER_REFRESH_TOKEN,
            data={"Token": token, "userDeviceId": user_device_id},
        )
        return resp

    async def data_latest(self) -> dict:
        resp: dict = await self._request("get", API_URL_SCAFFOLD, DATA_LATEST)
        return resp

    async def data_hour(self, serial_number: str, prev_date_time: str) -> dict:
        resp: dict = await self._request(
            "post",
            API_URL_SCAFFOLD,
            DATA_HOUR,
            data={"serialNumber": serial_number, "prevDateTime": prev_date_time},
        )
        return resp

    async def device_data(self, serial_number: str) -> dict:
        resp: dict = await self._request(
            "post", API_URL_SCAFFOLD, DEVICE_DATA, data={"serialNumber": serial_number}
        )
        return resp
