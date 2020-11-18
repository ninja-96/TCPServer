import socket
import selectors


class TCPServer:
    """
    ThreadTCPServer recv and send bytes or bytearray.
    Server use socketserver.ThreadingTCPServer.

    Examples::
        To define handler just @decorate handler method
            from TCPServer import TCPServer

            server = TCPServer('localhost', 5000)

            @server.handler
            def my_method(addr: tuple, data: bytes) -> (bytes, bytearray):
                print(f'{addr[0]}:{addr[1]} - {data}')
                return bytes(data)

            server.run()

        In console type 'nc localhost 5000' to send data
    """
    def __init__(self, host='localhost', port=5000, max_clients=10, bufsize=16):
        self.__selector = selectors.DefaultSelector()

        self.__reg_func = None
        self.__max_clients = max_clients
        self.__bufsize = bufsize

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen()

        self.__selector.register(fileobj=server, events=selectors.EVENT_READ, data=(self.__handler, server))

    def __handler(self, server):
        client, addr = server.accept()

        current_num_clients = len(self.__selector.get_map()) - 1
        if current_num_clients < self.__max_clients:
            self.__selector.register(fileobj=client, events=selectors.EVENT_READ, data=(self.__receive, client, addr))
        else:
            client.close()

    def __receive(self, client, addr):
        try:
            data = client.recv(self.__bufsize)

            if data:
                return_data = self.__reg_func(addr, data)

                if type(return_data) in [bytes, bytearray]:
                    try:
                        client.send(return_data)
                    except BrokenPipeError:
                        self.__selector.unregister(client)
                elif return_data is not None:
                    self.__selector.unregister(client)
                    raise TypeError('\'bytes\' or \'bytearray\' required')
            else:
                self.__selector.unregister(client)
                client.close()

        except ConnectionResetError:
            self.__selector.unregister(client)
            client.close()

    def run(self):
        if self.__reg_func is None:
            raise RuntimeError('Handler not specified')

        while True:
            events = self.__selector.select()

            for key, event in events:
                callback = key.data[0]
                callback(*key.data[1:])

    def handler(self, func):
        if self.__reg_func is None:
            self.__reg_func = func
        else:
            raise AttributeError(f'Method already associated')

        return self.__reg_func
