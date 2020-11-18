import socketserver


class ThreadTCPServer:
    """
    ThreadTCPServer recv and send bytes or bytearray.
    Server use socketserver.ThreadingTCPServer.

    Examples::
        To define handler just @decorate handler method
            from ThreadTCPServer import ThreadTCPServer

            server = ThreadTCPServer('localhost', 5000)

            @server.handler
            def my_method(addr: tuple, data: bytes) -> (bytes, bytearray):
                print(f'{addr[0]}:{addr[1]} - {data}')
                return bytes(data)

            server.run()

        In console type 'nc localhost 5000' to send data
    """
    def __init__(self, host='localhost', port=5000):
        self.__server = Server(host, port, BaseHandler)

    def run(self):
        if self.__server.get_func() is None:
            raise RuntimeError('Handler not specified')

        self.__server.serve_forever()

    def handler(self, func):
        if not self.__server.get_func():
            self.__server.set_func(func)
        else:
            raise AttributeError(f'Method already associated')


class Server(socketserver.ThreadingTCPServer):
    def __init__(self, host, port, handler):
        super().__init__((host, port), handler)
        self.__func = None

    def set_func(self, func):
        self.__func = func

    def get_func(self):
        return self.__func

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(request, client_address, self, self.__func)


class BaseHandler(socketserver.StreamRequestHandler):
    def __init__(self, request, addr, server, func):
        self.__func = func
        super(BaseHandler, self).__init__(request, addr, server)

    def handle(self):
        while True:
            data = self.request.recv(1024)
            if data:
                return_data = self.__func(self.client_address, data)

                if type(return_data) in [bytes, bytearray]:
                    try:
                        self.wfile.write(return_data)
                    except BrokenPipeError:
                        self.connection.close()
                        break
            else:
                self.connection.close()
                break
