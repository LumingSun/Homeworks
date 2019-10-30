from socket import *
import time
import random
def client():
    # HOST = '10.48.71.160'
    # HOST = '127.0.0.1'
    HOST = '10.77.110.234'
    PORT = 10521
    clientsocket = socket(AF_INET, SOCK_STREAM)         #AF_INET（对于IPV4协议的TCP和 UDP） SOCK_STREAM流套接字
    clientsocket.connect_ex((HOST, PORT))
    print("connection established")
    data = 1
    while(data ==1):
        try:
            data = int(clientsocket.recv(1024).decode())
            if(data ==1):
                print("wating for another player...")
        except:
            pass

    print("Game Begin!")
    my_data = input('开始：J--剪子,B--包袱,C--锤,R--Random\n')
    if(my_data == 'R'):
        my_data = random.choice(['J','B','C'])
        print(my_data)
    clientsocket.send(my_data.encode())
    judgement = clientsocket.recv(1024).decode()
    print(judgement)
    clientsocket.close()



while True:
    client()
    time.sleep(2)