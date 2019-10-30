# -.-coding:utf-8

import socket, traceback
import json
import threading


host = '127.0.0.1'
port = 51400
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
conn = {}
nick = {}
invite = {}
playing = {}
number = 0
def Get_Number():
    global conn
    global nick
    global invite
    global playing
    out = 1
    while out <= 1024:
        if(not conn.has_key(out)):
            return out
        out += 1
    conn = {}
    nick = {}
    invite = {}
    playing = {}
    out = 1
    return out

def thread_f():
    pass

while 1:
    try:
        message, address = s.recvfrom(8192)
        if('connect init' in message):
            number = Get_Number()
            if(number <= 1024):
                conn[number] = address
                nick_name = message[12:]
                nick[number] = nick_name.decode("utf-8")
            s.sendto("yours ID:", conn[number])
            s.sendto(str(number), conn[number])
            member_json = json.dumps(nick).encode("utf8")       #dict to string
            s.sendto(member_json, conn[number])
        elif(message == 'Quit'):
            tmp = [str(k) for k,v in conn.items() if v == address]           #my_id
            if len(tmp) > 0 :
                conn.pop(int(tmp[0]),"no")
                nick.pop(int(tmp[0]),"no")
                invite.pop(int(tmp[0]),'no')
        elif("Me" in message):
            tmp = [str(k) for k,v in invite.items() if str(v) == message[2:]]
            if len(tmp) > 0 :
                s.sendto("Invited"+str(tmp[0])+"    "+nick[int(tmp[0])],address)
                invite.pop(int(tmp[0]),"no")
            else :
                s.sendto("No",address)
        elif("Invite" in message):
            active_id = message[7:12].strip()
            passive_id = message[12:].strip()
            invite[int(active_id)] = passive_id
        elif("Accept" in message):
            active_id = message[6:11].strip()       #he
            passive_id = message[11:].strip()       #me
            s.sendto("Start"+str(passive_id)+"    "+nick[int(passive_id)],conn[int(active_id)])
            invite.pop(int(active_id),"no")
            playing[int(active_id)] = 0
            playing[int(passive_id)] = 0
        elif("Query" in message):
            query_id = message[5:].strip()
            if(playing.has_key(int(query_id))):
                if(playing[int(query_id)] == 0):
                    s.sendto('0',conn[int(query_id)])
                else:
                    send_json = json.dumps(playing[int(query_id)])
                    s.sendto(send_json,conn[int(query_id)])
                    playing[int(query_id)] = 0

        elif("W_i_n" in message):
            winner = message[5:10].strip()
            loser  = message[10:].strip()
            s.sendto("W_i_n",conn[int(loser)])
            playing.pop(int(winner),"no")
            playing.pop(int(loser),"no")
        else :
            data_list = json.loads(message)
            if(playing.has_key(int(data_list["His_ID"]))):
                playing[int(data_list["His_ID"])] = message

    except (KeyboardInterrupt, SystemExit):
        print "raise"
        raise
    except :
        print "traceback"
        traceback.print_exc()
