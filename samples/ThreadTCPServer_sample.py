import time
from ThreadTCPServer import ThreadTCPServer

server = ThreadTCPServer()
out_list = ['sample', 'test', 'list']


@server.handler(pass_list=out_list)
def test(addr: tuple, data: bytes, pass_list) -> (bytes, bytearray):
    print(pass_list)
    print(f'{addr[0]}:{addr[1]} - {data}')

    time.sleep(0.3)
    return bytes(data)


if __name__ == '__main__':
    server.run()
