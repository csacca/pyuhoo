import logging
from typing import Optional

from aiohttp import ClientSession

from .api import API
from .consts import APP_VERSION, CLIENT_ID
from .device import Device
from .util import encrypted_hash, json_pp, salted_hash


class Client(object):
    def __init__(self, username: str, password: str, websession: ClientSession, **kwargs) -> None:
        self._log: logging.Logger = logging.getLogger("pyuhoo")

        if kwargs.get("debug") is True:
            self._log.setLevel(logging.DEBUG)
            self._log.debug("Debug mode is explicitly enabled.")
        else:
            self._log.debug("Debug mode is not explicitly enabled (but may be enabled elsewhere).")

        self._app_version: int = APP_VERSION
        self._client_id: str = CLIENT_ID
        self._devices: dict = {}
        self._username: str = username
        self._password: str = password
        self._websession: ClientSession = websession
        self._refresh_token: Optional[str] = None
        self.user_settings_temp: str = "f"  # "f" or "c"

        self._api: API = API(self._websession)

    async def login(self) -> None:
        app_must_update: bool = await self._api.app_must_update(self._app_version)

        if app_must_update:
            self._log.debug(f"[login] need to update app version")

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

        self._refresh_token = user_login["refreshToken"]
        self._api.set_auth_token(self._refresh_token)

    async def get_latest_data(self) -> None:
        data_latest: dict = await self._api.data_latest()

        self.user_settings_temp = data_latest["userSettings"]["temp"]

        device: dict
        for device in data_latest["devices"]:
            serial_number: str = device["serialNumber"]
            if serial_number not in self._devices:
                self._devices[serial_number] = Device(device)

        for data in data_latest["data"]:
            serial_number: str = data["serialNumber"]
            device: Device = self._devices[serial_number]
            if device.timestamp < data["timestamp"]:
                device.update_data(data)

    def get_device(self, serial_number) -> Optional[Device]:
        if serial_number in self._devices:
            return self._devices[serial_number]
        else:
            return None

    def get_devices(self) -> dict:
        return self._devices
