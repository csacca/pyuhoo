import asyncio
import os

import pytest
from aiohttp import ClientSession

from pyuhoo.api import API
from pyuhoo.consts import CLIENT_ID

# from pprint import pprint


if os.getenv("USERNAME") is None:
    pytest.skip(
        "USERNAME not defined, live tests will fail. Skipping.", allow_module_level=True
    )

# if os.getenv("PASSWORD") is None:
#     pytest.skip(
#         "PASSWORD not defined, live tests will fail. Skipping.", allow_module_level=True
#     )


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
async def results(websession, username):

    _results = {}

    api: API = API(websession)

    user_config: dict = await api.user_config()
    _results["user_config"] = user_config

    # u_id = user_config["uId"]

    client_id = CLIENT_ID
    user_verify_email: dict = await api.user_verify_email(username, client_id)
    _results["user_verify_email"] = user_verify_email

    return _results


def test_user_config(results):
    user_config = results["user_config"]

    assert "uId" in user_config.keys()
    assert len(user_config.keys()) == 1


def test_user_verify_email(results):
    user_verify_email = results["user_verify_email"]

    assert "code" in user_verify_email.keys()
    assert "id" in user_verify_email.keys()
    assert len(user_verify_email.keys()) == 2
