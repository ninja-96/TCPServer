from TCPRequest import TCPRequest

status, data = TCPRequest.send('localhost', 5000, b'Hello world!')

print(data, status)
