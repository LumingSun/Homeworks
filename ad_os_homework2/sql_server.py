# -*- coding: UTF-8 -*-
from socket import *
import MySQLdb
def server():
    db = MySQLdb.connect("localhost","test" )
    cursor = db.cursor()                            #启动mysql connector
    cursor.execute("use test;")
    HOST = ''
    PORT = 10521
    ADDR = (HOST, PORT)
    server_socket = socket(AF_INET, SOCK_STREAM)        #调用socket构造函数，AF_UNIX(Unix域，用于同一台机器上的进程间通讯)，
                                                        # 也可以是AF_INET（对于IPV4协议的TCP和 UDP）套接字类型stream
    server_socket.bind(ADDR)                            #将socket绑定到指定地址
    server_socket.listen(5)                             #最大连接数5
    while True:
        print( 'Waiting for connecting ......')
        tcpclientsocket, addr = server_socket.accept()  #客户请求连接时，方法建立连接并返回服务器。 accept进入waiting状态
                                                        #topclientsocket是新的socket对象，服务器与其通信
        print('Connected by ', addr)
        while True:
            try:
                sql = tcpclientsocket.recv(1024).decode()
                print(sql)
                try:
                    cursor.execute(sql)
                    db.commit()
                except:
                    db.rollback()
                data_back = cursor.fetchall()
                print (data_back)
                tcpclientsocket.send(str(data_back))
            except:
                pass
        tcpclientsocket.close()
    server_socket.close()

server()