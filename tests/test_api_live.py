import asyncio
import os
from typing import List

import pytest
from aiohttp import ClientSession

from pyuhoo.api import API
from pyuhoo.consts import CLIENT_ID
from pyuhoo.util import encrypted_hash, salted_hash

#
# Configure expected dictionary keys
#

USER_CONFIG_KEYS = ["uId"]

USER_VERIFY_EMAIL_KEYS = ["code", "id"]

USER_LOGIN_KEYS = [
    "token",
    "refreshToken",
    "deviceId",
    "name",
    "lastname",
    "Role",
    "status",
    "gdpr",
    "language",
    "Roletype",
    "companyName",
    "clientName",
    "paymentStatus",
]

USER_REFRESH_TOKEN_KEYS = [
    "refreshToken",
    "token",
    "gdpr",
    "language",
    "Role",
    "paymentStatus",
]

DATA_LATEST_KEYS = ["devices", "data", "userSettings", "offline", "systemTime"]

DATA_LATEST_DATA_KEYS = [
    "serialNumber",
    "timestamp",
    "dust",
    "temp",
    "humidity",
    "pressure",
    "voc",
    "co2",
    "co",
    "ozone",
    "no2",
    "virusScore",
]
DATA_LATEST_DEVICES_KEYS = [
    "calibration",
    "city",
    "city_ios",
    "createdAt",
    "home",
    "latitude",
    "location",
    "longitude",
    "macAddress",
    "name",
    "offline",
    "serialNumber",
    "server",
    "ssid",
    "status",
    "threshold",
]


def verify_keys(expected: List["str"], returned: dict):
    for key in expected:
        assert key in returned

    extra_keys = set(returned.keys()) - set(expected)
    if len(extra_keys) > 0:
        print("EXTRA KEYS FOUND")
        print("================")
    for key in extra_keys:
        print(f"{key}={returned[key]}")

#
# Check if required environmental variables are defined
#

if os.getenv("UHOO_USERNAME") is None:
    pytest.skip(
        "UHOO_USERNAME not defined, live tests will fail. Skipping.",
        allow_module_level=True,
    )

if os.getenv("UHOO_PASSWORD") is None:
    pytest.skip(
        "UHOO_PASSWORD not defined, live tests will fail. Skipping.",
        allow_module_level=True,
    )


#
# Fixtures
#


@pytest.fixture(scope="module")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
async def websession():
    async with ClientSession() as _websession:
        yield _websession


@pytest.fixture(scope="module")
async def results(websession, username, password):

    _results = {}

    # Create API client
    api: API = API(websession)

    # do user_config()
    user_config: dict = await api.user_config()
    _results["user_config"] = user_config

    u_id = user_config["uId"]

    # do user_verify_email()
    client_id = CLIENT_ID
    user_verify_email: dict = await api.user_verify_email(username, client_id)
    _results["user_verify_email"] = user_verify_email

    code: str = user_verify_email["code"]
    id: str = user_verify_email["id"]

    # do user_login()
    salted: str = salted_hash(password, u_id)
    encrypted: str = encrypted_hash(code, salted)
    user_login: dict = await api.user_login(username, encrypted, id)
    _results["user_login"] = user_login

    device_id = user_login["deviceId"]
    token = user_login["token"]
    refresh_token = user_login["refreshToken"]
    api.set_bearer_token(refresh_token)

    # do user_refresh_token()
    user_refresh_token: dict = await api.user_refresh_token(token, device_id)
    _results["user_refresh_token"] = user_refresh_token

    token = user_refresh_token["token"]
    refresh_token = user_refresh_token["refreshToken"]
    api.set_bearer_token(refresh_token)

    # do data_latest()
    data_latest: dict = await api.data_latest()
    _results["data_latest"] = data_latest

    return _results


#
# Tests
#


def test_user_config(results):
    user_config: dict = results["user_config"]

    verify_keys(USER_CONFIG_KEYS, user_config)


def test_user_verify_email(results):
    user_verify_email: dict = results["user_verify_email"]

    verify_keys(USER_VERIFY_EMAIL_KEYS, user_verify_email)


def test_user_login(results):
    user_login: dict = results["user_login"]

    verify_keys(USER_LOGIN_KEYS, user_login)


def test_user_refresh_token(results):
    user_refresh_token: dict = results["user_refresh_token"]

    verify_keys(USER_REFRESH_TOKEN_KEYS, user_refresh_token)


def test_data_latest(results):
    data_latest: dict = results["data_latest"]

    verify_keys(DATA_LATEST_KEYS, data_latest)


def test_data_latest_data(results):
    data_latest: dict = results["data_latest"]

    assert "data" in data_latest.keys()

    if len(data_latest["data"]) > 0:
        data = data_latest["data"][0]
        verify_keys(DATA_LATEST_DATA_KEYS, data)
    else:
        pytest.skip('Skipping: No data to test in data_latest["data"]')


def test_data_latest_devices(results):
    data_latest: dict = results["data_latest"]

    assert "devices" in data_latest.keys()

    if len(data_latest["devices"]) > 0:
        devices = data_latest["devices"][0]
        verify_keys(DATA_LATEST_DEVICES_KEYS, devices)
    else:
        pytest.skip('Skipping: No devices to test in data_latest["devices"]')
