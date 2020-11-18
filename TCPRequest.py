import socket


class TCPRequest:
    """
    Easy to use TCPRequest wrapper
    Examples::
        from TCPRequest import TCPRequest

        connector = TCPRequest('localhost', 5000)
        ret = connector.send(b'Hello world')
        print(ret)

        ret = connector.send_recv(b'Hello world')
        print(ret)
    """
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, data, timeout=None):
        """
        Send data to server
        :param data: data bytes or bytearray
        :param timeout: send timeout
        :return: Number of send bytes
        """
        try:
            self.__connection.connect((self.__host, self.__port))
        except ConnectionRefusedError:
            return 0

        if timeout is None:
            self.__connection.settimeout(timeout)

        try:
            self.__connection.send(data)
            self.__connection.close()
            return len(data)
        except BrokenPipeError:
            self.__connection.close()
            return 0
        except socket.timeout:
            return 0

    def send_recv(self, data, bufsize=1024, timeout=None):
        """
        Send and receive data from server
        :param data: data bytes or bytearray
        :param bufsize: receive length
        :param timeout: send timeout
        :return: received data or 'None' if receive wes failed
        """
        try:
            self.__connection.connect((self.__host, self.__port))
        except ConnectionRefusedError:
            return None

        if timeout is None:
            self.__connection.settimeout(timeout)

        try:
            self.__connection.send(data)
            self.__connection.close()
        except BrokenPipeError:
            self.__connection.close()
            return None

        try:
            data = self.__connection.recv(bufsize)
            self.__connection.close()
            return data

        except socket.timeout:
            self.__connection.close()
            return None
