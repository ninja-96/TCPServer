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
    def __init__(self, host='localhost', port=5000, bufsize=16):
        self.__server = Server(host, port, BaseHandler, bufsize)

    def run(self):
        if self.__server.get_func() is None:
            raise RuntimeError('Handler not specified')

        self.__server.serve_forever()

    def handler(self, *args, **kwargs):
        def decorator(func):
            if not self.__server.get_func():
                self.__server.set_func(func)
                self.__server.set_args(args)
                self.__server.set_kwargs(kwargs)

        return decorator


class Server(socketserver.ThreadingTCPServer):
    def __init__(self, host, port, handler, bufsize):
        super().__init__((host, port), handler)

        self.__func = None
        self.__args = None
        self.__kwargs = None
        self.__bufsize = bufsize

    def set_args(self, args):
        self.__args = args

    def get_args(self):
        return self.__args

    def set_kwargs(self, kwargs):
        self.__kwargs = kwargs

    def get_kwargs(self):
        return self.__kwargs

    def set_func(self, func):
        self.__func = func

    def get_func(self):
        return self.__func

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(request, client_address, self, self.__bufsize, self.__func, self.__args, self.__kwargs)


class BaseHandler(socketserver.StreamRequestHandler):
    def __init__(self, request, addr, server, bufsize, func, args, kwargs):
        self.__func = func
        self.__args = args
        self.__kwargs = kwargs
        self.__bufsize = bufsize
        super(BaseHandler, self).__init__(request, addr, server)

    def handle(self):
        while True:
            data = self.request.recv(self.__bufsize)
            if data:
                return_data = self.__func(self.client_address, data, *self.__args, **self.__kwargs)

                if type(return_data) in [bytes, bytearray]:
                    try:
                        self.wfile.write(return_data)
                    except BrokenPipeError:
                        self.connection.close()
                        break
            else:
                self.connection.close()
                break
