from TCPServer import TCPServer

server = TCPServer(echo=False)

@server
def test(addr, data):
    print(f'{addr} : {data}')

    return bytes(data)


if __name__ == '__main__':
    server.run()
