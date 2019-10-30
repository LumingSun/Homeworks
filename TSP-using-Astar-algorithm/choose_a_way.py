import math
from collections import Counter
import random
def ave(total_city_num, now_city_num, cities, my_map):   #总城市数，目前的城市，所有城市的Node，距离map表
    number = 0
    sum = 0
    city_list = []
    for i in range(0, total_city_num):     #记录并计数 number是未在close表的总城市数
        if ( cities[i].close == 0 ):
            number = number + 1
            #print(i,"不在close表中",number)
            city_list.append(i)             #city_list是目前尚未进入close表的城市代号 从0开始！
    for city in city_list:              #city是数字
        sum = my_map[now_city_num][city] + sum
        #print(now_city_num,city)
    average = sum/number
    return average

def my_min(node,city_list,my_map):
    my_min = 1000000
    for city in city_list:
        if city == node:
            pass
        elif my_map[node][city]<my_min:
            my_min = my_map[node][city]
    return my_min

def choose_f_min(total_city_num, now_city_num, cities, my_map,means,max_in_map,min_in_map):             #sort
    city_list = []                           #city_list是目前尚未进入close表的城市代号 从0开始！
    now_city_average = []
    g = {}
    h = {}
    f = {}
    number = 0
    for i in range(0, total_city_num):     #记录并计数 number是未在close表的总城市数
        if ( cities[i].close == 0 ):
            number = number + 1
            #print(i,"不在close表中")
            city_list.append(i)
    #print("现在的节点是：", now_city_num)
    #print("可以去的节点数量为:", number)
    for city in city_list:
        g[city] = my_map[city][now_city_num]
        average = ave(total_city_num, city, cities, my_map)             # 1=average,2=number*average,3=sqrt(number*average)
        if means == 1:
            h[city] = average
        elif means == 2:
            h[city] = now_city_num * average
        elif means == 3:
            h[city] = math.sqrt(now_city_num * average)
        elif means == 4:
            h[city] = my_min(city,city_list,my_map)
        elif means == 5:
            h[city] = now_city_num * my_min(city,city_list,my_map)
        elif means == 6:
            h[city] = math.sqrt(now_city_num * my_min(city,city_list,my_map))
        elif means == 7:
            h[city] = random.uniform(min_in_map,max_in_map)
        elif means == 8:
            h[city] = 0
        elif means == 9:
            h[city] = math.sqrt(now_city_num * average)+math.sqrt(now_city_num * my_min(city,city_list,my_map))
        G,H = Counter(g),Counter(h)
        f = dict(G+H)
        #print("现在的节点是",now_city_num,"当下一个节点是：",city,"f是：",f[city],"g是：",g[city],"h是：",h[city])
    r = sorted(f.items(), key=lambda x: x[1], reverse=False)                     # r 是排序后的字典，要选出r的第一个返回
    #print("g is",g)
    #print("h is",h)
    #print("f is",f)
    #print('next node:',r[0][0])
    #print("***********************************")
    return r[0][0]

def name_of_means(i):
    if i == 1:
        return ("average")
    elif i == 2:
        return ("now_city_num * average")
    elif i == 3:
        return ("sqrt(now_city_num * average)")
    elif i == 4:
        return ("my_min(city,city_list,my_map)")
    elif i == 5:
        return ("now_city_num * my_min")
    elif i == 6:
        return ("sqrt(now_city_num * my_min)")
    elif i == 7:
        return ("random")
    elif i == 8:
        return ("h = 0")

