import asyncio

import aiohttp

from .settings import PASSWORD, USERNAME


async def main():
    async with aiohttp.ClientSession() as session:
        await run(session, USERNAME, PASSWORD)


async def run(session, username, password):
    pass


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main)
