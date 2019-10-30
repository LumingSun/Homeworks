from socket import *

def judge(player_1, player_2):
    if(player_1 == player_2):
        return 0
    elif(player_1== 'J'and player_2== 'B'):
        return 1
    elif(player_1== 'C' and player_2 == 'J'):
        return 1
    elif(player_1== 'B' and player_2 == 'C'):
        return 1
    else:
        return 2

def server():
    HOST = ''
    PORT = 10521
    ADDR = (HOST, PORT)
    server_socket = socket(AF_INET, SOCK_STREAM)        #调用socket构造函数，AF_UNIX(Unix域，用于同一台机器上的进程间通讯)，
                                                        # 也可以是AF_INET（对于IPV4协议的TCP和 UDP）套接字类型stream
    server_socket.bind(ADDR)                            #将socket绑定到指定地址
    server_socket.listen(2)                             #最大连接数1
    print( 'Waiting for connecting ......')
    tcpclientsocket, addr = server_socket.accept()  #客户请求连接时，方法建立连接并返回服务器。 accept进入waiting状态#topclientsocket是新的socket对象，服务器与其通信
    print('Connected by play1', addr)
    info = '1'
    tcpclientsocket.send(info.encode())
    tcpclientsocket_2, addr_2 = server_socket.accept()
    print('Connected by play2', addr_2)
    info = '2'
    tcpclientsocket.send(info.encode())
    tcpclientsocket_2.send(info.encode())        #ready
    play_1 = tcpclientsocket.recv(1024).decode()
    play_2 = tcpclientsocket_2.recv(1024).decode()
    print(play_1,play_2)
    judgement = judge(play_1,play_2)
    if(judgement == 0):
        info = '平局'
        tcpclientsocket.send(info.encode())
        tcpclientsocket_2.send(info.encode())
    elif(judgement == 1):
        tcpclientsocket.send("Win!".encode())
        tcpclientsocket_2.send("Lose out".encode())
    else:
        tcpclientsocket.send("Lose out".encode())
        tcpclientsocket_2.send("Win!".encode())
    server_socket.close()
while True:
    server()