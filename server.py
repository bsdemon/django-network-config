from email import message
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
        
    # GET return JSON
    def do_GET(self):
        self.respond('GET')
    
    # POST return JSON
    def do_POST(self):
        self.respond('POST')

    def respond(self, arg0):
        delay = random.randint(1,20)
        time.sleep(delay)
        json_msg = json.dumps({'Status': 'OK', 'Methond': arg0})
        self._set_headers()
        self.wfile.write(bytes(json_msg, encoding='utf8'))
        
def run(server_class=HTTPServer, handler_class=Server, port=8008):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    
    print ('Starting httpd on port %d...' % port)
    httpd.serve_forever()
    
if __name__ == "__main__":
    from sys import argv
    
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()