from TCPRequest import TCPRequest, send_ones, send_recv_ones

if __name__ == '__main__':
    connector = TCPRequest('localhost', 5000)

    ret = connector.send(b'Hello world', timeout=10)
    print(ret)

    ret = connector.send_recv(b'Hello world', bufsize=128, timeout=10)
    print(ret)

    ret = send_ones('localhost', 5000, b'Hello world', timeout=10)
    print(ret)

    ret = send_recv_ones('localhost', 5000, b'Hello world', bufsize=128, timeout=10)
    print(ret)
