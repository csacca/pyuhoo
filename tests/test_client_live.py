import asyncio
import os

import pytest
from aiohttp import ClientSession

from pyuhoo import Client

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
async def client(websession, username, password):
    return Client(username, password, websession)

def test_get_latest_data(client: Client):
    client.get_latest_data()