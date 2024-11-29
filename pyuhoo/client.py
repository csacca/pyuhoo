import logging
from typing import Dict, Optional

from aiohttp import ClientSession

from pyuhoo.errors import ForbiddenError, RequestError, UhooError, UnauthorizedError

from .api import API
from .consts import APP_VERSION, CLIENT_ID
from .device import Device
from .util import encrypted_hash, json_pp, salted_hash


class Client(object):
    def __init__(
        self, username: str, password: str, websession: ClientSession, **kwargs
    ) -> None:
        self._log: logging.Logger = logging.getLogger("pyuhoo")

        if kwargs.get("debug") is True:
            self._log.setLevel(logging.DEBUG)
            self._log.debug("Debug mode is explicitly enabled.")
        else:
            self._log.debug(
                "Debug mode is not explicitly enabled (but may be enabled elsewhere)."
            )

        self._app_version: int = APP_VERSION
        self._client_id: str = CLIENT_ID
        self._device_id: Optional[str] = None
        self._devices: Dict[str, Device] = {}
        self._username: str = username
        self._password: str = password
        self._websession: ClientSession = websession
        self._token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        # This *seems* to be defaulted to 'c' now.
        self.user_settings_temp: str = "c"  # "f" or "c"

        self._api: API = API(self._websession)

    async def login(self) -> None:
        # app_must_update: bool = await self._api.app_must_update(self._app_version)

        # if app_must_update:
        #     self._log.debug("[login] need to update app version")

        user_config: dict = await self._api.user_config()
        self._log.debug(f"[user_config] returned\n{json_pp(user_config)}")
        u_id = user_config["uId"]

        user_verify_email: dict = await self._api.user_verify_email(
            self._username, self._client_id
        )
        self._log.debug(f"[user_verify_email] returned\n{json_pp(user_verify_email)}")
        code: str = user_verify_email["code"]
        id: str = user_verify_email["id"]

        salted: str = salted_hash(self._password, u_id)
        self._log.debug(f"[login] using salted hash {salted}")

        encrypted: str = encrypted_hash(code, salted)
        self._log.debug(f"[login] using encrypted hash {encrypted}")

        user_login: dict = await self._api.user_login(self._username, encrypted, id)
        self._log.debug(f"[user_login] returned\n{json_pp(user_login)}")

        self._device_id = user_login["deviceId"]
        self._token = user_login["token"]
        self._refresh_token = user_login["refreshToken"]
        self._api.set_bearer_token(self._refresh_token)

    async def refresh_token(self) -> None:
        """FIXME: user_refresh_token doesn't seem to work once token is expired..."""
        if self._token is None:
            raise UhooError("Error cannot refresh token prior to logging in")

        try:
            user_refresh_token: dict = await self._api.user_refresh_token(
                self._token, self._device_id
            )

            self._log.debug(
                f"[user_refresh_token] returned\n{json_pp(user_refresh_token)}"
            )

            self._token = user_refresh_token["token"]
            self._refresh_token = user_refresh_token["refreshToken"]
            self._api.set_bearer_token(self._refresh_token)

        except RequestError as e:
            self._log.debug(
                "\033[91m"
                + "[refresh_token] received {} error, attempting to re-login".format(type(e))
                + "\033[0m"
            )
            self._api.set_bearer_token(None)
            await self.login()

    async def get_latest_data(self) -> None:
        try:
            data_latest: dict = await self._api.data_latest()
        except RequestError as e:
            self._log.debug(
                "\033[93m"
                + "[get_latest_data] received {} error, refreshing token and trying again".format(type(e))
                + "\033[0m"
            )
            await self.refresh_token()
            data_latest = await self._api.data_latest()

        #self._log.debug(f"[data_latest] returned\n{json_pp(data_latest)}")

        if "temp" in data_latest.get("userSettings",{}):
            self.user_settings_temp = data_latest["userSettings"]["temp"]

        device: dict
        for device in data_latest["devices"]:
            serial_number: str = device["serialNumber"]
            if serial_number not in self._devices:
                self._devices[serial_number] = Device(device)

            data = device["data"]

            serial_number = data["serialNumber"]
            device_obj: Device = self._devices[serial_number]
            if device_obj.timestamp < data["timestamp"]:
                device_obj.update_data(data)

    def get_device(self, serial_number) -> Optional[Device]:
        if serial_number in self._devices:
            return self._devices[serial_number]
        else:
            return None

    def get_devices(self) -> Dict[str, Device]:
        return self._devices
