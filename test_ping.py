#! venv/bin/python
from asyncio import tasks
import ipaddress
import asyncio
from pyclbr import Function
from unittest import result
import aioping

# ip_range = list(ipaddress.IPv4Network('1.0.0.0/8'))
# ip_range = list(ipaddress.IPv4Network('1.0.0.0/16'))
ip_range = list(ipaddress.IPv4Network('1.0.0.0/24'))
batch = 64
count = 0
print(len(ip_range))
print(ip_range[0], ip_range[-1])

def send_32(ip_range):
    return ip_range[:32] if len(ip_range) > 32 else ip_range

async def do_ping(host):
    try:
        delay = await aioping.ping(str(host), timeout=10) * 1000
        print(f"Ping response {host} in {delay} ms")
    except TimeoutError:
        print(f" - {host} Timed out -")


async def run_tasks(ip_range):
    while len(ip_range)>0 :
        ip_range_32 = send_32(ip_range)
        tasks = [do_ping(ip) for ip in ip_range_32]
        await asyncio.gather(*tasks)
        await asyncio.sleep(1)
        ip_range = ip_range[32:]

if __name__ =="__main__":
    asyncio.run(run_tasks(ip_range))


