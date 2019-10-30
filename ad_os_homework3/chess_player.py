# -.-encoding:utf-8

import pygame
from pygame.locals import *
import socket
import sys
import json
import Tkinter

host = '127.0.0.1'
textport = 51400

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    port = int(textport)
except ValueError:
    port = socket.getservbyname(textport, 'udp')

His_Nick = 0
My_Nick  = 0
My_ID    = 0
His_ID   = 0

link = 0
Waiting = 1
pygame.init()
Width  = 595
Height = 665
SCREEN_SIZE = (Width, Height)
board_size = (Width+14, Height)

imgpath = 'img/'
edge = 16
distance = 66


Is_Run = 0
can = []
sit = [[0 for i in range(9)] for i in range(10)]
FPS = 10
fpsClock = pygame.time.Clock()
BLACK = (0 , 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0, 200)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BACKGROUP = (178,118,42)


O_O   = pygame.image.load(imgpath+"OO.GIF")
O_O_S = pygame.image.load(imgpath+"OOS.GIF")

screen = 0


chessboardimg = pygame.image.load(imgpath+'chessboard.GIF')
chessboardimg = pygame.transform.scale(chessboardimg, board_size)

win = pygame.image.load(imgpath+"win.png")
fail = pygame.image.load(imgpath+"fail.png")

Me = 'B'
He = 'R'


clock = 0
Is_Win = 0

def loc_2_pos(locate):
    pos_c = (locate[0]-edge-20)/distance
    pos_c_rem = (locate[0]-edge-20)%distance
    if pos_c_rem > 20 and pos_c_rem < 45 :
        return [999,999]        
    if pos_c_rem > 45 :
        pos_c += 1
    if ((locate[0]-edge-20) < 0):
        pos_c = 0

    if (locate[1] < edge+20+distance*5):
        pos_r = (locate[1]-edge-20)/distance
        pos_r_rem = (locate[1]-edge-20)%distance
        if pos_r_rem > 20 and pos_r_rem < 45:
            return [999,999]
        if pos_r_rem > 45 :
            pos_r += 1
        if ((locate[1]-edge-20) < 0):
            pos_r = 0
    else:
        pos_r = (locate[1]-edge-20-10)/distance
        pos_r_rem = (locate[1]-edge-20-10)%distance
        if pos_r_rem > 20 and pos_r_rem < 45:
            return [999,999]
        if pos_r_rem > 45 :
            pos_r += 1

    return [pos_r,pos_c]

def pos_2_loc(pos):
    if(pos[0]<=5):
        return [pos[1]*distance+edge,pos[0]*distance+edge]
    if(pos[0]>5):
        return [pos[1]*distance+edge,pos[0]*distance+edge]

def reg_sit(pos,value):
    # pos
    sit[pos[0]][pos[1]] = value

def unreg_sit(pos):
    # pos
    sit[pos[0]][pos[1]] = blank("OO.GIF","OOS.GIF",(pos[0],pos[1]),He) 

def sit_2_value(pos):
    # sit
    return sit[pos[1]][pos[0]]

def go_step(old,new):
    sit[old[0]][old[1]].update(new)
    #Obj_Selected.update(pos)

def recv_step():
    try:
        buf_json = s.recv(4096)
        return buf_json
    except :
        recv_step()

def load_step(step_json):
    global Waiting
    step_list = json.loads(step_json)
    step_list = json.loads(step_list)
    old_pos = step_list['old']
    new_pos = step_list['new']
    old = [9-int(old_pos[0]),8-int(old_pos[1])]
    new = [9-int(new_pos[0]),8-int(new_pos[1])]
    go_step(old,new)
    Waiting = 0

def Win():
    global Is_Win
    Is_Win = 1
    screen.blit(win,(150,250))

def Fail():
    global Is_Win
    Is_Win = -1
    screen.blit(fail,(150,250))

def query_step():
    s.sendall("Query"+str(My_ID))
    step = recv_step()
    if(step != '0' and step != 'No'):
        if(step == "W_i_n"):
            Fail()
            return
        load_step(step)

def send_step(old,new):
    data_list = {'His_ID':His_ID,
                 'old' : old,
                 'new' : new}
    data_json = json.dumps(data_list)
    s.sendall(data_json)

def leave():
    if(My_ID != 0):
        s.sendall("Quit")
    exit()



class chess:
    def __init__(self,item_img,item_s_img,pos,color):
        self.item   = pygame.image.load(imgpath+item_img)
        self.item_s = pygame.image.load(imgpath+item_s_img)
        self.pos = pos
        self.color = color
        if(color != Me):
            self.item   = pygame.transform.flip(self.item,True,True)
            self.item_s = pygame.transform.flip(self.item_s,True,True)
        self.over = 0
        self.focus = 0
        self.can = []
        self.candicas = 0
        
        self.update()
    def select(self):
        self.lock()
        if(self.focus == 0):
            self.next_step()
            self.show_step()
            self.focus = 1
            return
        if(self.focus == 1):
            self.show_step()
            self.can = []
            self.focus = 0
        

    def lock(self):
        tmp = self.item
        self.item = self.item_s
        self.item_s = tmp
        

    def next_step(self):
        pass

    def show_step(self):
        for self.candicas in range(len(self.can)):
            self.can[self.candicas].lock()

    def remove(self):
        unreg_sit(self.pos)
        self.over = 1

    def update(self,pos=[99,99]):
        if(pos != [99,99]):
            unreg_sit(self.pos)
            self.pos = pos
        reg_sit(self.pos,self)
        screen.blit(self.item,pos_2_loc(self.pos))

class A(chess):
    def next_step(self):
        if(self.pos[1] % 2 == 1):
            if(sit[8][4].color != Me):
                self.can.append(sit[8][4])
        else:
            if(sit[7][3].color != Me):
                self.can.append(sit[7][3])

            if(sit[7][5].color != Me):
                self.can.append(sit[7][5])

            if(sit[9][3].color != Me):
                self.can.append(sit[9][3])

            if(sit[9][5].color != Me):
                self.can.append(sit[9][5])

class B(chess):
    def next_step(self):
        self.can = [sit[5][2],sit[5][6],sit[7][0],sit[7][4],sit[7][8],sit[9][2],sit[9][6]]
        self.can.remove(sit[self.pos[0]][self.pos[1]])        
        for self.candicas in self.can:
            if(abs(self.pos[0] - self.candicas.pos[0]) != 2):
                self.can[self.can.index(self.candicas)] = 0
                continue
            if(abs(self.pos[1] - self.candicas.pos[1]) != 2):
                self.can[self.can.index(self.candicas)] = 0
                continue
            if(self.candicas.color == Me):
                self.can[self.can.index(self.candicas)] = 0
                continue
            if(not isinstance(sit[(self.pos[0]+self.candicas.pos[0])/2][(self.pos[1]+self.candicas.pos[1])/2],blank)):
                self.can[self.can.index(self.candicas)] = 0
                continue

        while 0 in self.can :
            self.can.remove(0)

class C(chess):
    def next_step(self):
        tmp_pos = [self.pos[0],self.pos[1]]
        bed = 0
        if(tmp_pos[0] != 9):
            tmp_pos[0] += 1
        while tmp_pos[0] <= 9 :
            if bed == 0:
                if(isinstance(sit[tmp_pos[0]][tmp_pos[1]],blank)):
                    self.can.append(sit[tmp_pos[0]][tmp_pos[1]])
                if(not isinstance(sit[tmp_pos[0]][tmp_pos[1]],blank)):
                    bed = sit[tmp_pos[0]][tmp_pos[1]]
            else:
                if(not isinstance(sit[tmp_pos[0]][tmp_pos[1]],blank)):
                    if(sit[tmp_pos[0]][tmp_pos[1]].color != Me):
                        self.can.append(sit[tmp_pos[0]][tmp_pos[1]])
                    break

            tmp_pos[0] += 1
            
        tmp_pos = [self.pos[0],self.pos[1]]
        bed = 0
        if(tmp_pos[0] != 0):
            tmp_pos[0] -= 1
        while tmp_pos[0] >= 0 :
            if bed == 0:
                if(isinstance(sit[tmp_pos[0]][tmp_pos[1]],blank)):
                    self.can.append(sit[tmp_pos[0]][tmp_pos[1]])
                if(not isinstance(sit[tmp_pos[0]][tmp_pos[1]],blank)):
                    bed = sit[tmp_pos[0]][tmp_pos[1]]
            else:
                if(not isinstance(sit[tmp_pos[0]][tmp_pos[1]],blank)):
                    if(sit[tmp_pos[0]][tmp_pos[1]].color != Me):
                        self.can.append(sit[tmp_pos[0]][tmp_pos[1]])
                    break
                    
            tmp_pos[0] -= 1

        tmp_pos = [self.pos[0],self.pos[1]]
        bed = 0
        if(tmp_pos[1] != 8):
            tmp_pos[1] += 1
        while tmp_pos[1] <= 8 :
            if bed == 0:
                if(isinstance(sit[tmp_pos[0]][tmp_pos[1]],blank)):
                    self.can.append(sit[tmp_pos[0]][tmp_pos[1]])
                if(not isinstance(sit[tmp_pos[0]][tmp_pos[1]],blank)):
                    bed = sit[tmp_pos[0]][tmp_pos[1]]
            else:
                if(not isinstance(sit[tmp_pos[0]][tmp_pos[1]],blank)):
                    if(sit[tmp_pos[0]][tmp_pos[1]].color != Me):
                        self.can.append(sit[tmp_pos[0]][tmp_pos[1]])
                    break

            tmp_pos[1] += 1 
            
        tmp_pos = [self.pos[0],self.pos[1]]
        bed = 0
        if(tmp_pos[1] != 0):
            tmp_pos[1] -= 1
        while tmp_pos[1] >= 0 :
            if bed == 0:
                if(isinstance(sit[tmp_pos[0]][tmp_pos[1]],blank)):
                    self.can.append(sit[tmp_pos[0]][tmp_pos[1]])
                if(not isinstance(sit[tmp_pos[0]][tmp_pos[1]],blank)):
                    bed = sit[tmp_pos[0]][tmp_pos[1]]
            else:
                if(not isinstance(sit[tmp_pos[0]][tmp_pos[1]],blank)):
                    if(sit[tmp_pos[0]][tmp_pos[1]].color != Me):
                        self.can.append(sit[tmp_pos[0]][tmp_pos[1]])
                    break
                    
            tmp_pos[1] -= 1

class K(chess):
    def lock(self):
        tmp = self.item
        self.item = self.item_s
        self.item_s = tmp     
        if(self.color != Me):
            s.sendall("W_i_n"+str(My_ID)+"    "+str(His_ID))
            Win()

    def next_step(self):
        self.can = [sit[self.pos[0]-1][self.pos[1]],
               sit[self.pos[0]][self.pos[1]-1],
               sit[self.pos[0]][self.pos[1]+1]]
        if(self.pos[0] < 9):
            self.can.append(sit[self.pos[0]+1][self.pos[1]])

        for self.candicas in self.can :
            if(self.candicas.pos[0] not in [7,8,9] or self.candicas.pos[1] not in [3,4,5] or self.candicas.color == Me):
                self.can[self.can.index(self.candicas)] = 0
                continue

        while 0 in self.can :
            self.can.remove(0)

class N(chess):
    def next_step(self):
        x_tmp = self.pos[0]
        y_tmp = self.pos[1]
        x_list = [x_tmp-2,x_tmp-1,x_tmp+1,x_tmp+2]
        y_list = [y_tmp-2,y_tmp-1,y_tmp+1,y_tmp+2]

        if(self.pos[0] > 0 and not isinstance(sit[self.pos[0]-1][self.pos[1]],blank)):
            x_list.remove(x_tmp-2)
        if(self.pos[0] < 9 and not isinstance(sit[self.pos[0]+1][self.pos[1]],blank)):
            x_list.remove(x_tmp+2)

        if(self.pos[1] > 0 and not isinstance(sit[self.pos[0]][self.pos[1]-1],blank)):
            y_list.remove(y_tmp-2)
        if(self.pos[1] < 8 and not isinstance(sit[self.pos[0]][self.pos[1]+1],blank)):
            y_list.remove(y_tmp+2)

        self.can = [sit[i][j] for i in x_list for j in y_list \
                    if i>=0 and i<=9 and j>=0 and j<=8]

        for self.candicas in self.can:
            if(abs(self.candicas.pos[0] - self.pos[0]) == abs(self.candicas.pos[1] - self.pos[1])):
                self.can[self.can.index(self.candicas)] = 0
                continue

            if(self.candicas.color == Me):
                self.can[self.can.index(self.candicas)] = 0
                continue

        while 0 in self.can :
            self.can.remove(0)

class P(chess):
    def next_step(self):
        if self.pos[0]-1 >= 0 and sit[self.pos[0]-1][self.pos[1]].color != Me :
            self.can.append(sit[self.pos[0]-1][self.pos[1]])
        if self.pos[0] <= 4 :
            if self.pos[1]-1 >= 0 and sit[self.pos[0]][self.pos[1]-1].color != Me :
                self.can.append(sit[self.pos[0]][self.pos[1]-1])
            if self.pos[1]+1 <= 8 and sit[self.pos[0]][self.pos[1]+1].color != Me :
                self.can.append(sit[self.pos[0]][self.pos[1]+1])
 
class R(chess):
    def next_step(self):
        tmp_pos = [self.pos[0],self.pos[1]]
        if(tmp_pos[0] != 9):
            tmp_pos[0] += 1
        while tmp_pos[0] <= 9 :
            if(sit[tmp_pos[0]][tmp_pos[1]].color != Me):
                self.can.append(sit[tmp_pos[0]][tmp_pos[1]])
            if(not isinstance(sit[tmp_pos[0]][tmp_pos[1]],blank)):
                break
            tmp_pos[0] += 1
            
        tmp_pos = [self.pos[0],self.pos[1]]
        if(tmp_pos[0] != 0):
            tmp_pos[0] -= 1
        while tmp_pos[0] >= 0 :
            if(sit[tmp_pos[0]][tmp_pos[1]].color != Me):
                self.can.append(sit[tmp_pos[0]][tmp_pos[1]])
            if(not isinstance(sit[tmp_pos[0]][tmp_pos[1]],blank)):
                break
            tmp_pos[0] -= 1 

        tmp_pos = [self.pos[0],self.pos[1]]
        if(tmp_pos[1] != 8):
            tmp_pos[1] += 1
        while tmp_pos[1] <= 8 :
            if(sit[tmp_pos[0]][tmp_pos[1]].color != Me):
                self.can.append(sit[tmp_pos[0]][tmp_pos[1]])
            if(not isinstance(sit[tmp_pos[0]][tmp_pos[1]],blank)):
                break
            tmp_pos[1] += 1 
            
        tmp_pos = [self.pos[0],self.pos[1]]
        if(tmp_pos[1] != 0):
            tmp_pos[1] -= 1
        while tmp_pos[1] >= 0 :
            if(sit[tmp_pos[0]][tmp_pos[1]].color != Me):
                self.can.append(sit[tmp_pos[0]][tmp_pos[1]])
            if(not isinstance(sit[tmp_pos[0]][tmp_pos[1]],blank)):
                break
            tmp_pos[1] -= 1 

class blank(chess):
    def next_step(self):
        pass

def begin_game():
    global screen
    global sit
    global Is_Run
    global Waiting
    global Me
    global He
    global clock
    global Is_Win
    Is_Win = 0

    if Me == 'B':
        Waiting = 1
        He = 'R'
    else :
        Waiting = 0
        He = 'B'

    Is_Run = 1
    screen = pygame.display.set_mode(SCREEN_SIZE, 0 ,32)
    sit = [[blank("OO.GIF","OOS.GIF",(j,i),He) for i in range(9)] for j in range(10)]

    if (Me == 'B'):
        B_R_L = R("BR.GIF","BRS.GIF",(9,0),'B')     #車
        B_R_R = R("BR.GIF","BRS.GIF",(9,8),'B')
        B_N_L = N("BN.GIF","BNS.GIF",(9,1),'B')     #马
        B_N_R = N("BN.GIF","BNS.GIF",(9,7),'B')
        B_B_L = B("BB.GIF","BBS.GIF",(9,2),'B')     #象
        B_B_R = B("BB.GIF","BBS.GIF",(9,6),'B')
        B_A_L = A("BA.GIF","BAS.GIF",(9,3),'B')     #士
        B_A_R = A("BA.GIF","BAS.GIF",(9,5),'B')
        B_C_L = C("BC.GIF","BCS.GIF",(7,1),'B')     #炮
        B_C_R = C("BC.GIF","BCS.GIF",(7,7),'B')
        B_P_L = P("BP.GIF","BPS.GIF",(6,0),'B')     #卒
        B_P_T = P("BP.GIF","BPS.GIF",(6,2),'B')
        B_P_M = P("BP.GIF","BPS.GIF",(6,4),'B')
        B_P_F = P("BP.GIF","BPS.GIF",(6,6),'B')
        B_P_R = P("BP.GIF","BPS.GIF",(6,8),'B')
        B_K   = K("BK.GIF","BKS.GIF",(9,4),'B')     #将

        R_K   = K("RK.GIF","RKS.GIF",(0,4),'R')     #帥
        R_R_L = R("RR.GIF","RRS.GIF",(0,0),'R')     #車
        R_R_R = R("RR.GIF","RRS.GIF",(0,8),'R')
        R_N_L = N("RN.GIF","RNS.GIF",(0,1),'R')     #马
        R_N_R = N("RN.GIF","RNS.GIF",(0,7),'R')
        R_B_L = B("RB.GIF","RBS.GIF",(0,2),'R')     #象
        R_B_R = B("RB.GIF","RBS.GIF",(0,6),'R')
        R_A_L = A("RA.GIF","RAS.GIF",(0,3),'R')     #士
        R_A_R = A("RA.GIF","RAS.GIF",(0,5),'R')
        R_C_L = C("RC.GIF","RCS.GIF",(2,1),'R')     #炮
        R_C_R = C("RC.GIF","RCS.GIF",(2,7),'R')
        R_P_L = P("RP.GIF","RPS.GIF",(3,0),'R')     #兵
        R_P_T = P("RP.GIF","RPS.GIF",(3,2),'R')
        R_P_M = P("RP.GIF","RPS.GIF",(3,4),'R')
        R_P_F = P("RP.GIF","RPS.GIF",(3,6),'R')
        R_P_R = P("RP.GIF","RPS.GIF",(3,8),'R')  
    else :
        B_K   = K("BK.GIF","BKS.GIF",(0,4),'B')     #将
        B_R_L = R("BR.GIF","BRS.GIF",(0,0),'B')     #車
        B_R_R = R("BR.GIF","BRS.GIF",(0,8),'B')
        B_N_L = N("BN.GIF","BNS.GIF",(0,1),'B')     #马
        B_N_R = N("BN.GIF","BNS.GIF",(0,7),'B')
        B_B_L = B("BB.GIF","BBS.GIF",(0,2),'B')     #象
        B_B_R = B("BB.GIF","BBS.GIF",(0,6),'B')
        B_A_L = A("BA.GIF","BAS.GIF",(0,3),'B')     #士
        B_A_R = A("BA.GIF","BAS.GIF",(0,5),'B')
        B_C_L = C("BC.GIF","BCS.GIF",(2,1),'B')     #炮
        B_C_R = C("BC.GIF","BCS.GIF",(2,7),'B')
        B_P_L = P("BP.GIF","BPS.GIF",(3,0),'B')     #卒
        B_P_T = P("BP.GIF","BPS.GIF",(3,2),'B')
        B_P_M = P("BP.GIF","BPS.GIF",(3,4),'B')
        B_P_F = P("BP.GIF","BPS.GIF",(3,6),'B')
        B_P_R = P("BP.GIF","BPS.GIF",(3,8),'B')
        
        R_K   = K("RK.GIF","RKS.GIF",(9,4),'R')     #帥
        R_R_L = R("RR.GIF","RRS.GIF",(9,0),'R')     #車
        R_R_R = R("RR.GIF","RRS.GIF",(9,8),'R')
        R_N_L = N("RN.GIF","RNS.GIF",(9,1),'R')     #马
        R_N_R = N("RN.GIF","RNS.GIF",(9,7),'R')
        R_B_L = B("RB.GIF","RBS.GIF",(9,2),'R')     #象
        R_B_R = B("RB.GIF","RBS.GIF",(9,6),'R')
        R_A_L = A("RA.GIF","RAS.GIF",(9,3),'R')     #士
        R_A_R = A("RA.GIF","RAS.GIF",(9,5),'R')
        R_C_L = C("RC.GIF","RCS.GIF",(7,1),'R')     #炮
        R_C_R = C("RC.GIF","RCS.GIF",(7,7),'R')
        R_P_L = P("RP.GIF","RPS.GIF",(6,0),'R')     #兵
        R_P_T = P("RP.GIF","RPS.GIF",(6,2),'R')
        R_P_M = P("RP.GIF","RPS.GIF",(6,4),'R')
        R_P_F = P("RP.GIF","RPS.GIF",(6,6),'R')
        R_P_R = P("RP.GIF","RPS.GIF",(6,8),'R')

    Obj_Selected = 0
    pygame.display.set_caption(My_Nick+" VS "+His_Nick)
    while True :
        screen.fill(BACKGROUP)
        screen.blit(chessboardimg,(2,2))

        for i in range(10):
            for j in range(9):
                sit[i][j].update()

        if(Is_Win == 1):
            Win()
        elif(Is_Win == -1):
            Fail()


        clock = (clock+1)%10 
        if(Waiting == 1 and clock == 9 and Is_Win == 0):
            query_step()

        for event in pygame.event.get() :
            if event.type == QUIT :
                pygame.quit()
                leave()
                Is_Run = 0 
                
                break
            if(Is_Win != 0):
                continue
            if event.type == 5 and Waiting == 0:
                if(event.pos[0] > 20 and event.pos[1] > 20 and event.pos[0] < Width-20 and event.pos[1] < Height-20):
                    select_pos = loc_2_pos(event.pos)
                    if(select_pos[0] != 999):
                        if(sit[select_pos[0]][select_pos[1]].color == Me):
                            if (Obj_Selected != 0):
                                Obj_Selected.select()
                            Obj_Selected = sit[select_pos[0]][select_pos[1]]
                            Obj_Selected.select()
                        else:
                            if (Obj_Selected != 0):            # go_step
                                if (sit[select_pos[0]][select_pos[1]] in Obj_Selected.can):
                                    send_step(Obj_Selected.pos,select_pos)
                                    Waiting = 1
                                    go_step(Obj_Selected.pos,select_pos)
                                    sit[select_pos[0]][select_pos[1]].select()
                                    Obj_Selected = 0

        if(Is_Run == 0):
            break
        pygame.display.update()
        fpsClock.tick(FPS)

def Go_Start():

    begin_game()

def send_invite(event=None):
    s.sendall("Invited"+My_ID+"    "+His_ID)
    link.configure(state="disable") 
    link.configure(text="Waiting for Accepttion")
    link.unbind("<ButtonRelease-1>")
    member.unbind('<Double-Button-1>')

def select_or_invite(info):
    global His_Nick
    global His_ID
    His_ID = info[0:4].strip()
    His_Nick = info[5:].strip()
    nick_name.set(His_Nick)
    link.configure(state="normal")
    link.bind("<Double-Button-1>")

def accept_invite(event=None):
    s.sendall("Accept"+His_ID+"    "+My_ID)
    Go_Start()

def recv_invite():
    global Is_Run
    global His_ID
    global His_Nick
    global Me
    if(Is_Run == 0):
        s.sendall("Me"+str(My_ID))
        invite_info = s.recv(4096)
        if('Invited' in invite_info):       #Invited1
            select_or_invite(invite_info[7:])
            link.configure(text="Accept Invitation")
            link.unbind("<ButtonRelease-1>")
            link.bind("<ButtonRelease-1>",accept_invite)
        elif('No' == invite_info):
            root.after(1000,recv_invite)
        elif('Start' in invite_info):
            His_ID = int(invite_info[5:10].strip())
            His_Nick = invite_info[10:].strip()
            Me ='R'
            Go_Start()
            Is_Run = 1
        else:
            Is_Run = 1

def select_player(event=None):
    player_info = member.get(member.curselection()).strip() #1    RanFeng
    select_or_invite(player_info)
    link.configure(text="Invite He")
    link.unbind("<ButtonRelease-1>")
    link.bind("<ButtonRelease-1>",send_invite)

def show_online():
    nick.configure(state="disable")
    nick.unbind("<Button-1>")
    nick.unbind('<Key>')

    member_json = recv_step()
    member_list = json.loads(member_json.decode("utf-8"))
    list_item = [[k,v] for k,v in member_list.items() if k != My_ID]
    for item in list_item:
        member.insert(Tkinter.END, item[0]+"    "+item[1])

    recv_invite()

def link_server(event):
    global link
    global My_ID

    My_Nick = nick.get().strip()
    if(My_Nick == '' or My_Nick == u"请输入昵称"):
        nick_name.set("请输入昵称")
        link.configure(state="disable")
        link.unbind("<ButtonRelease-1>")
        return

    s.connect((host, port))

    s.sendall("connect init"+My_Nick.encode("utf8"))
    if(recv_step() == 'yours ID:'):
        My_ID = recv_step()
        link.configure(state="disable") 
        link.unbind("<ButtonRelease-1>")
        show_online()

def Get_Nick(event):
    global nick
    global link
    if(nick.get().strip() == u"请输入昵称"):
        nick.delete(0, Tkinter.END)
    elif(nick.get().strip() != ''):
        link.configure(state="normal")
        link.bind("<ButtonRelease-1>",link_server)

def input_nickname(event):
    global link
    global My_Nick
    My_Nick = nick.get().strip()
    if My_Nick != '' and My_Nick != u"请输入昵称":
        link.configure(state="normal")
        link.bind("<ButtonRelease-1>",link_server)
    else:
        link.configure(state="disable")
        link.unbind("<ButtonRelease-1>")

def show_ui():
    global link
    global member
    global nick
    global nick_name
    global root
    root = Tkinter.Tk()
    root.configure(background='#B0000A')
    root.title("AD_OS_象棋")
    root.geometry('280x280')
    root.resizable(width=False, height=False)

    nick_name = Tkinter.StringVar()
    nick = Tkinter.Entry(root,textvariable=nick_name,state='normal')
    nick_name.set("请输入昵称")
    
    nick.place(x=80,y=5)
    nick.bind("<Button-1>",Get_Nick)
    nick.bind('<Key>', input_nickname)

    link = Tkinter.Button(root,text="Link The Server")
    link.place(x=100,y=40)
    link.configure(state="disable")

    member = Tkinter.Listbox(root)
    member.place(x=80,y=90)
    member.bind('<Double-Button-1>', select_player)

    root.protocol("WM_DELETE_WINDOW", leave)
    root.mainloop()

show_ui()
