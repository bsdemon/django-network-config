from django.core.management.base import BaseCommand
import asyncio
import aiohttp

class Command(BaseCommand):
    help = 'Dispatch config'
    url = 'http://localhost:{}'


    def add_arguments(self, parser):
        parser.add_argument('port', type=str, help='Indicates port number')

    async def handle(self, *args, **kwargs):
        port = kwargs['port']
        async with aiohttp.ClientSession() as session:
            await self.make_single_task(self, session, port)

    async def make_single_task(self, session, port):
        await session.get(self.url.format(port))
        print(f'Task on port {port} is done')   