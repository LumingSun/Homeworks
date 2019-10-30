from socket import *
def client():
    HOST = '127.0.0.1'
    PORT = 10521
    clientsocket = socket(AF_INET, SOCK_STREAM)         #AF_INET（对于IPV4协议的TCP和 UDP） SOCK_STREAM流套接字
    clientsocket.connect((HOST, PORT))
    while True:
        data = input('Client>>>')
        clientsocket.send(data.encode())
        data = clientsocket.recv(1024)
        print(data)
client()