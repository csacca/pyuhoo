import asyncio
import logging
from os import getenv

from aiohttp import ClientSession
from dotenv import load_dotenv

from pyuhoo import Client

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

username = getenv("PYUHOO_USERNAME")
password = getenv("PYUHOO_PASSWORD")


async def init_client(username, password, websession) -> Client:
    return Client(username, password, websession, debug=True)


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
        client: Client = await init_client(username, password, websession)

        await client.login()

        await client.get_latest_data()

        devices = client.get_devices()
        device = next(iter(devices.values()))  # get reference to first/arbitrary device

        print(
            f"{device.serial_number}\n  {device.datetime}\n  "
            + f"{device.temp} {client.user_settings_temp}\n"
        )

        await asyncio.sleep(2 * 60)  # wait 2 minutes, server updates values once every 60 seconds

        await client.get_latest_data()  # polls/updates all devices

        print(
            f"{device.serial_number}\n  {device.datetime}\n  "
            + f"{device.temp} {client.user_settings_temp}\n"
        )


asyncio.get_event_loop().run_until_complete(main())
