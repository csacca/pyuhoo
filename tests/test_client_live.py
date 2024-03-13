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

async def test_get_latest_data(username, password):
    async with ClientSession() as _websession:
        client = Client(username, password, _websession)
        await client.login()
        data = await client.get_latest_data()
    pass