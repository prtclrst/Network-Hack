import aiohttp
import asyncio
# import requests # sync library. delays by response time (latency)
import time

'''
Simultaneous single HTTP GET request by async I/O.
Load test for many requests per sec & total requests counts.

Modern web servers have defense mechanisms in place to combat traffic spikes, such as rate limiting, IP blocking, WAF, and Cloudflare. 
'''

async def send_request(session, url): 
# prepare for request failures or blocks due to server protection : network error, timeout, server ban (block access), etc.
    try:
        async with session.get(url) as response: # aiohttp async request
            print(f"Status: {response.status}")
            # response.status : 429 - rate limiting, 403 - block, etc.
    except Exception as e:
        print(f"Error: {e}")

async def main():
    target = r"https://bezier-calulator.web.app/"
    num_requests = int(input("Number of requests: ")) # test URL & requests counts

    print(f"Starting test on {target} with {num_requests} requests...")
    start_time = time.time()

    timeout = aiohttp.ClientTimeout(total=5) # 5s timeout to break if request takes too much time
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [send_request(session, target) for _ in range(num_requests)]
        await asyncio.gather(*tasks) # execute many coroutines in parallel

    # time_elapse
    print(f"Test completed in {time.time() - start_time:.2f} seconds") 

if __name__ == "__main__":
    asyncio.run(main())

'''
TODO
1. 단순히 GET 요청만 반복적으로 보내는 것은 서버에 큰 부담 X. POST, HEAD 등 다양한 요청 유형과 리소스 소모가 큰 대용량 데이터 요청 따위를 포함해야 효과적
서버의 특정 리소스 (CPU 집약적 API)를 타겟팅하도록 수정해보자.
2. 예외 처리 강화
3. distributed sys such as botnet
4. multithread
'''
