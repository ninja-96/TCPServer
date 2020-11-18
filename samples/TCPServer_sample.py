import time
from TCPServer import TCPServer

server = TCPServer()


@server.handler
def test(addr: tuple, data: bytes) -> (bytes, bytearray):
    print(f'{addr[0]}:{addr[1]} - {data}')

    time.sleep(0.3)
    return bytes(data)


if __name__ == '__main__':
    server.run()