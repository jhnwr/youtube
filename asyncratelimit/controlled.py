from aiolimiter import AsyncLimiter
import asyncio
import httpx

async def request_data(client, url, limiter):
    async with limiter:
        resp = await client.get(url)
        print(resp.json())
        return resp.json()


async def main():
    rate_limit = AsyncLimiter(100, 0.1)
    async with httpx.AsyncClient() as client:
        tasks = []
        for url in urls:
            tasks.append(request_data(client, "http://localhost:4000/", rate_limit))
        data = await asyncio.gather(*tasks)
    return data


urls = [i for i in range(1, 1000)]
results = asyncio.run(main())
errors = sum([1 for e in results if 'Error' in e.values()])
sucesses = sum([1 for e in results if 'Successful' in e.values()])
output = {"sucesses": sucesses, "errors": errors}
print(output)

