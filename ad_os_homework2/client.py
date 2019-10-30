# -*- coding: UTF-8 -*-
from socket import *
def client():
    HOST = '192.168.40.129'
    PORT = 10521
    clientsocket = socket(AF_INET, SOCK_STREAM)         #AF_INET（对于IPV4协议的TCP和 UDP） SOCK_STREAM流套接字
    clientsocket.connect((HOST, PORT))
    while True:
        data = raw_input('Client>>>')
        clientsocket.send(data.encode())
        data = clientsocket.recv(1024)
        print(data)
# client()

def connect():
    user_name = raw_input("Please input your name:...\n")
    password = raw_input("Please input your password:...\n")
    if (user_name =="slm" and password =="slm"):
        HOST = '192.168.40.129'
        PORT = 10521
        clientsocket = socket(AF_INET, SOCK_STREAM)         #AF_INET（对于IPV4协议的TCP和 UDP） SOCK_STREAM流套接字
        clientsocket.connect((HOST, PORT))
        print("database connected\n")
        return clientsocket
    else:
        print("Wrong! User name and password don't match, please try again.")
        connect()
def select(clientsocket):
    print("********************************************************************************************")
    print("                           choose the attribute you want to select                           ")
    print("        0--empno    1--first name   2--last_name    3--hire_date    4--more                  ")
    print("********************************************************************************************")
    search_way = int(raw_input())
    if(search_way == 0):
        empno = raw_input("The empno you want to select...\n")
        sql = "select * from employees where emp_no = "+ empno + ';'
        clientsocket.send(sql.encode())
    elif(search_way == 1):
        first_name = raw_input("The first name you want to select...\n")
        sql = "select * from employees where first_name = '" + first_name + '\';'
        clientsocket.send(sql.encode())
    elif(search_way == 2):
        last_name = raw_input("The last name you want to select...\n")
        sql = "select * from employees where last_name = '"+ last_name +'\';'
        clientsocket.send(sql.encode())
    elif(search_way == 3):
        hire_date = raw_input("The hire date you want to select...\n")
        sql = "select * from employees where hire_date = '"+ hire_date + '\';'
        clientsocket.send(sql.encode())
    elif(search_way == 4):
        sql = raw_input("Input you sql for select...\n")
        clientsocket.send(sql.encode())
    else:
        print("wrong number")
        return 0
    data = clientsocket.recv(4096)
    try:
        output = data.lstrip('(').rstrip(')').split("), (")
        for each in output:
            print(each)
    except:
        print(data)

def insert(clientsocket):
    param = raw_input("Data you want to insert:...\n")
    sql = "insert into employees (emp_no,birth_date,first_name,last_name,gender,hire_date) values(" + param + ");"
    print("finished,",sql)
    clientsocket.send(sql.encode())
    data = clientsocket.recv(4096)
    print(data)

def delete(clientsocket):
    param = raw_input("emp_no you want to delete:...\n")
    sql = "delete from employees where emp_no =" + param
    print("finished,",sql)
    clientsocket.send(sql.encode())
    data = clientsocket.recv(4096)
    print(data)


def more(clientsocket):
    sql = raw_input("please input the SQL ")
    clientsocket.send(sql.encode())
    data = clientsocket.recv(4096)
    try:
        output = data.lstrip('(').rstrip(')').split("), (")
        for each in output:
            print(each)
    except:
        print(data)


def init():
    print("********************************************************************************************")
    print("                            welcom to employee manage system                                ")
    print("********************************************************************************************")
    socket = connect()

    return socket
if __name__ == '__main__':
    socket = init()
    while(True):
        print("********************************************************************************************")
        print("                         Action:  1--查询   2--新增   3--删除   4--More                    ")
        print("********************************************************************************************")
        action = int(raw_input("I want to ...\n"))
        if (action==1):
            select(socket)
        elif (action==2):
            insert(socket)
        elif (action==3):
            delete(socket)
        elif (action==4):
            more(socket)
        else:
            print("wrong number...please try again")

