import aiohttp
import asyncio
import time

start_time = time.time()

import os
import dotenv
dotenv.load_dotenv()
un1 = os.getenv('VTOP_USERNAME_2')
p1 = os.getenv('VTOP_PASSWORD_2')+"34"
un2 = os.getenv('VTOP_USERNAME')
p2 = os.getenv('VTOP_PASSWORD')
details = ((un1, p1), (un2, p2))
URL = "http://127.0.0.1:5000/api/v1/alldetails"


async def get_pokemon(session, url, data):
    async with session.post(url, data=data) as resp:
        return await resp.json()

async def main():

    async with aiohttp.ClientSession() as session:

        tasks = []
        for username, passwd in details:
            data = {
                'username': username,
                'password': passwd
            }
            tasks.append(asyncio.ensure_future(get_pokemon(session, URL, data)))

        original_pokemon = await asyncio.gather(*tasks)
        for pokemon in original_pokemon:
            print("-"*30)
            print(pokemon)

asyncio.run(main())
print("--- %s seconds ---" % (time.time() - start_time))