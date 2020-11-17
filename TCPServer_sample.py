from TCPServer import TCPServer
import time

server = TCPServer()


@server.handler
def test(addr, data):
    print(f'{addr[0]}:{addr[1]} - {data}')

    time.sleep(0.3)
    return bytes(data)


if __name__ == '__main__':
    server.run()
