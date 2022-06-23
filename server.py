# from aiohttp import web
# import os
# import asyncio
# import random
# import logging

# logging.basicConfig(
#     format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
#     datefmt='%d-%m-%Y:%H:%M:%S',
#     level=logging.ERROR #change to DEBUG or INFO for debuging
# )
# logger = logging.getLogger()

# async def handle(request):
#     await asyncio.sleep(random.uniform(0, 0.1))
#     return web.Response(text="Hi ")

# async def init():
#     app = web.Application()
#     app.router.add_route('POST', '/', handle)
#     return await loop.create_server(
#         app.make_handler(), '0.0.0.0', 8008)

# if __name__ == '__main__':

#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(init())
#     loop.run_forever()

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import random
import time


class Server(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        self.respond('GET')

    def do_POST(self):
        self.respond('POST')

    def respond(self, arg0):
        delay = random.randint(10, 30)
        time.sleep(delay)
        ok_resp = {'Status': 'Ok', 'Methond': arg0, 'Delay': delay}
        err_resp = {'Status': 'Error', 'Methond': arg0, 'Delay': delay,
                    'Message': 'Unrecognized command: `copy running-configuration startup-configuration`'}
        json_msg = json.dumps(ok_resp)
        if delay > 15 and delay < 25:
            json_msg = json.dumps(err_resp)
        self._set_headers()
        self.wfile.write(bytes(json_msg, encoding='utf8'))


def run(server_class=HTTPServer, handler_class=Server, port=8008):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    print('Starting httpd on port %d...' % port)
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
