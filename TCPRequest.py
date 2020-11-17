import socket


class TCPRequest:
    @staticmethod
    def send(host, port, data, bufsize=16, timeout=None):
        transmit = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            transmit.connect((host, port))
        except ConnectionRefusedError as e:
            return False, None

        try:
            transmit.send(data)
        except BrokenPipeError:
            transmit.close()
            return False, None

        if timeout is not None:
            transmit.settimeout(float(timeout))

        try:
            data = transmit.recv(bufsize)

            transmit.close()
            return True, data
        except socket.timeout:
            transmit.close()
            return False, None
