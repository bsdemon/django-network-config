import asyncio
import aiohttp
from sanic import Sanic, response

app = Sanic("Test Sanic ")

@app.route('/api/create_task', methods=['POST'])
async def get_ressource(request):
    ip = request.json['ip']
    url = f'http://{ip}:8008'
    asyncio.ensure_future(set_task(url))

async def set_task(url):
    conn = aiohttp.TCPConnector(verify_ssl=False)
    async with aiohttp.ClientSession(connector=conn, trust_env=True) as session:
        async with session.post(url) as resp:
            result = await resp.text()
    print(result)
