import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.0.7', 6240))

while True:
    data = '240|90|GeneralResult|MachineLearntResult|ClientStatus'
    sock.send(data)
    print "response: ", sock.recv(1024)