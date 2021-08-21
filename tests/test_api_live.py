import pytest
from aiohttp import ClientSession

from pyuhoo.api import API


@pytest.fixture
async def websession():
    async with ClientSession() as websession:
        yield websession


async def test_user_config(websession, loop):
    api = API(websession)
    user_config = await api.user_config()
    assert "uId" in user_config.keys()
    # assert len(user_config.keys()) == 1
