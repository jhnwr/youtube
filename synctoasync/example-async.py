import httpx
import asyncio

async def request_data(client, url):
    resp = await client.get(url)
    return resp.json()['name']


async def main():
    async with httpx.AsyncClient() as client:
        tasks = []
        for i in range(1,50):
            tasks.append(request_data(client, f"https://rickandmortyapi.com/api/character/{i}"))

        characters = await asyncio.gather(*tasks)
        for c in characters:
            print(c)


asyncio.run(main())

