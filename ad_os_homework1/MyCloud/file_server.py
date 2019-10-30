# -*- coding=utf-8 -*-

import socket
import threading
import time
import sys
import os
import struct


def socket_service():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', 6666))
    s.listen(10)
    print 'Waiting connection...'

    while 1:
        conn, addr = s.accept()
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()

def deal_data(conn, addr):
    print 'Accept new connection from {0}'.format(addr)
    conn.send('Hi, Welcome to the MingPan!')

    while 1:
        fileinfo_size = struct.calcsize('128sl')
        buf = conn.recv(fileinfo_size)
        if buf:
            filename, filesize = struct.unpack('128sl', buf)
            fn = filename.strip('\00')
            new_filename = os.path.join('./', fn + str(time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))))
            print 'file new name is {0}, filesize if {1}'.format(new_filename,
                                                                 filesize)

            recvd_size = 0  # 定义已接收文件的大小
            fp = open(new_filename, 'wb')
            print 'start receiving...'

            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = conn.recv(1024)
                    recvd_size += len(data)
                else:
                    data = conn.recv(filesize - recvd_size)
                    recvd_size = filesize
                fp.write(data)
            fp.close()
            print 'end receive...'
        conn.close()
        break


if __name__ == '__main__':
    socket_service()