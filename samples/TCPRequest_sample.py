from TCPRequest import TCPRequest

if __name__ == '__main__':
    connector = TCPRequest('localhost', 5000)

    ret = connector.send(b'Hello world')
    print(ret)

    ret = connector.send_recv(b'Hello world')
    print(ret)
