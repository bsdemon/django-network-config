from datetime import datetime
from django.core.management.base import BaseCommand
import asyncio
import aiohttp
from netaddr import IPRange


class Command(BaseCommand):
    help = 'Dispatch config'
    timeout_seconds = 10

    def add_arguments(self, parser):
        parser.add_argument('start_range', type=str, help='First ip in range')
        parser.add_argument('end_range', type=str, help='Last ip in range')

    async def make_task(self, session, ip_addr, port=8008):
        url = f'http://{ip_addr}:{port}'
        try:
            async with session.get(url) as stream_resp:
                resp = await stream_resp.text()
                print(f'Task on {url} is done with {resp}')

        except (asyncio.TimeoutError, aiohttp.ClientConnectorError) as e:
            now = datetime.now()
            print(f'#ERROR {now} {url} TIMEOUT ')
            return None
        except Exception as e:
            pass

    def handle(self, *args, **kwargs):
        async def _main():
            start_range = kwargs['start_range']
            end_range = kwargs['end_range']

            connector = aiohttp.TCPConnector(
                limit=0,
                verify_ssl=False,
                fingerprint=None,
                ttl_dns_cache=0,
                use_dns_cache=False,
                resolver=None,
            )

            session_timeout = aiohttp.ClientTimeout(total=None, sock_connect=self.timeout_seconds,
                                                    sock_read=self.timeout_seconds)

            if start_range == end_range:
                async with aiohttp.ClientSession(connector=connector, timeout=session_timeout) as session:
                    await self.add_task(session, start_range)
            else:
                async with aiohttp.ClientSession(connector=connector, timeout=session_timeout) as session:
                    ip_range = list(IPRange(start_range, end_range))
                    tasks = [self.make_task(session, ip) for ip in ip_range]
                    await asyncio.gather(*tasks, return_exceptions=True)
        asyncio.run(_main())
