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

@pytest.fixture()
def expected_lingering_timers() -> bool:
    """Temporary ability to bypass test failures.
    Parametrize to True to bypass the pytest failure.
    @pytest.mark.parametrize("expected_lingering_timers", [True])
    This should be removed when all lingering timers have been cleaned up.
    """
    return True

async def test_get_latest_data(username, password, expected_lingering_timers):
    async with ClientSession() as _websession:
        client = Client(username, password, _websession)
        await client.login()
        await client.get_latest_data()

    devices = client.get_devices()
    for device in devices.values():
        print(device)
