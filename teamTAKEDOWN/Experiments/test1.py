import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.0.7', 6000))

while True:
    data = '0|1000|GeneralResult|MachineLearntResult|ClientStatus'
    sock.send(data)
    print "response: ", sock.recv(1024)