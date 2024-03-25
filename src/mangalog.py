from my_http_server import MyHTTPServer
from request_handler import RequestHandler

def run(server_class=MyHTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    
    print(f'Starting server on port {port}...\n')
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        print("Server stopped.")

if __name__ == '__main__':
    run()
