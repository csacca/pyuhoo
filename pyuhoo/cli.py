import asyncio
import logging

import click
from aiohttp import ClientSession

from pyuhoo import Client


async def init_client(username, password, websession) -> Client:
    return Client(username, password, websession, debug=False)


async def example(username, password):
    async with ClientSession() as websession:
        client: Client = await init_client(username, password, websession)

        print("[-] Logging in")
        await client.login()
        print("[+] Successfully logged in")

        print("[-] Getting latest data")
        await client.get_latest_data()
        print("[+] Successfully received data")

        devices = client.get_devices()
        device = next(iter(devices.values()))  # get reference to first device

        print("[+] Data from first device:")
        print(
            f"    Serial Number: {device.serial_number}\n"
            + f"    Timestamp:     {device.datetime}\n"
            + f"    Temperature:   {device.temp} {client.user_settings_temp}\n"
        )

        while True:
            delay = 60 * 5
            print(f"[-] Sleeping for {delay} seconds...")
            await asyncio.sleep(delay)

            print("[-] Getting latest data")
            await client.get_latest_data()  # polls/updates all devices
            print("[+] Successfully received data")

            print("[+] Data from first device:")
            print(
                f"    Serial Number: {device.serial_number}\n"
                + f"    Timestamp:     {device.datetime}\n"
                + f"    Temperature:   {device.temp} {client.user_settings_temp}\n"
            )


@click.command()
@click.option("--username", "-u", prompt=True, help="uHoo username")
@click.option(
    "--password",
    "-p",
    prompt=True,
    hide_input=True,
    confirmation_prompt=False,
    help="uHoo password",
)
@click.option("--debug", is_flag=True)
def cli(username, password, debug):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARN)

    asyncio.get_event_loop().run_until_complete(example(username, password))


if __name__ == "__main__":
    cli()
    print("[+] Done!")
