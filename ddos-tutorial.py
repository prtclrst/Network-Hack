import aiohttp
import asyncio
import time

async def send_request(session, url):
    try:
        async with session.get(url) as response:
            print(f"Status: {response.status}")
    except Exception as e:
        print(f"Error: {e}")

async def main():
    target = r"https://bezier-calulator.web.app/"
    num_requests = int(input("Number of requests: "))

    print(f"Starting test on {target} with {num_requests} requests...")
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, target) for _ in range(num_requests)]
        await asyncio.gather(*tasks)

    print(f"Test completed in {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
