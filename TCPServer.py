import socket
import selectors


class TCPServer:
    def __init__(self, host='localhost', port=5000, max_clients=10, echo=False):
        self.__selector = selectors.DefaultSelector()

        self.__reg_func = None
        self.__max_clients = max_clients

        self.__echo = echo

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen()

        self.__selector.register(fileobj=server, events=selectors.EVENT_READ, data=(self.__handler, server))

    def __handler(self, server):
        client, addr = server.accept()

        current_num_clients = len(self.__selector.get_map()) - 1
        if current_num_clients < self.__max_clients:
            self.__selector.register(fileobj=client, events=selectors.EVENT_READ, data=(self.__recieve, client, addr))
        else:
            client.close()

    def __recieve(self, client, addr):
        data = client.recv(1024)

        if data:
            return_data = self.__reg_func(addr, data)

            if type(return_data) in [bytes, bytearray]:
                client.send(return_data)
            else:
                self.__selector.unregister(client)
                raise TypeError('\'bytes\' or \'bytearray\' required')
        elif self.__echo:
            client.send(data)
        else:
            self.__selector.unregister(client)
            client.close()

    def run(self):
        while True:
            events = self.__selector.select()

            for key, event in events:
                callback = key.data[0]
                callback(*key.data[1:])

    def __call__(self, *args, **kwargs):
        if self.__reg_func is None:
            self.__reg_func = args[0]
        else:
            raise AttributeError(f'Method already associated')

        return self.__reg_func
