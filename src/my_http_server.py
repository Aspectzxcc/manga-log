from http.server import HTTPServer

class MyHTTPServer(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)

    def serve_forever(self):
        try:
            super().serve_forever()
        except KeyboardInterrupt:
            print("Server shutting down...")
            self.server_close()
