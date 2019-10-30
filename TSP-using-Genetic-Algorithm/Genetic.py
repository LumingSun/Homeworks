import random
import numpy as np

def tsp_to_map(input_file):
    import math
    data = open(input_file)
    total_city_number = 0
    ID =[]
    xcoor = []
    ycoor = []
    for line in data:
        line = line.replace('\n', '')
        line = (line.split(" "))
        ID.append(int(line[0]))
        xcoor.append(float(line[1]))
        ycoor.append(float(line[2]))
        total_city_number = total_city_number+1
    dist_map = np.zeros((total_city_number,total_city_number))
    for m in range(0,total_city_number):
        for n in range(0,total_city_number):
            dist_map[m][n] = math.sqrt(math.pow(xcoor[m]-xcoor[n],2)+math.pow(ycoor[m]-ycoor[n],2))
    # np.savetxt(output_file,dist_map)
    return dist_map,total_city_number

def initial(total_city_number):
    #返回初始种群个数和n个初始顺序
    initial_list_number = int(total_city_number*10)              #开始时的种群个数
    initial_list = range(total_city_number)
    randomList= []
    for i in range(1,initial_list_number+1):
        randomList.append(random.sample(initial_list, total_city_number))
        # print(randomIndex)
    # print("initial",initial_list_number)
    print(len(randomList))
    return initial_list_number,randomList

def my_distance(total_city_number, list, my_map):
    #返回某一顺序的距离
    dis = 0
    for i in range(0,total_city_number-1):
        dis = dis + my_map[list[i] - 1][list[i + 1] - 1]
    dis = dis + my_map[list[total_city_number - 1] - 1][0]
    return dis

# def judge(total_city_number,list,my_map):
#     #返回路径的评价
#     dis = my_distance(total_city_number,list,my_map)
#     judgement = dis
#     return judgement

def cross(total_city_number, new1, new2):
    #杂交
    old1 = copy_list(new1)
    old2 = copy_list(new2)
    new1 = copy_list(new1)
    new2 = copy_list(new2)
    start = random.randint(0,total_city_number-1)
    end = random.randint(start,total_city_number-1)
    # print(start,end)
    father = old1[start:end+1]
    mother = old2[start:end+1]
    length = len(mother)
    for i in range(start,end+1):
        temp = new1[i]
        new1[i] = new2[i]
        new2[i] = temp         #list1 and list2 changed father and mother
    for i in range(0,start):
        while new1[i] in mother:
            for j in range(0,length):
                if(new1[i] == mother[j]):
                    new1[i] = father[j]
    for i in range(end+1,total_city_number):
        while new1[i] in mother:
            for j in range(0,length):
                if(new1[i] == mother[j]):
                    new1[i] = father[j]
    for i in range(0,start):
        while new2[i] in father:
            for j in range(0,length):
                if(new2[i] == father[j]):
                    new2[i] = mother[j]
    for i in range(end+1,total_city_number):
        while new2[i] in father:
            for j in range(0,length):
                if(new2[i] == father[j]):
                    new2[i] = mother[j]
    # print("old",old1,old2)
    # print("new", new1, new2)
    return new1, new2

def variation(total_city_number,list):
    #变异
    i = random.randint(0,total_city_number-1)
    j = random.randint(0,total_city_number-1)
    temp = list[i]
    list[i] = list[j]
    list[j] = temp
    return list

def calculate_judge_of_each_generation(lists_number,total_city_number,list_of_lists):
    judge_result = []
    new_list = []
    value_list = []
    key_list = []
    for i in range(0,lists_number):
        judge_result.append(my_distance(total_city_number,list_of_lists[i],my_map))
        new_list.append([judge_result[i],list_of_lists[i]])
    sorted_list = sorted(new_list, key=lambda x: x[0])
    for each in sorted_list:
        key_list.append(each[0])
        value_list.append(each[1])
    print(key_list)
    # print(key_list)
    # print(value_list)
    # dictionary = dict(new_list)                                                   WRONG!!!!!!
    # items = sorted(dictionary.items(), key=lambda x:x[0], reverse=False)
    # for i in range(0,len(items)):
    #     each = items[i]
    #     key_list.append(each[0])
    #     value_list.append(each[1])
    # print(sorted(value_list)==sorted(list_of_lists))
    # print()
    # print(key_list)
    return lists_number,value_list,key_list          #value_list 从小到大排序的访问顺序list  list of list

def copy_list(list):
    copyed_list = []
    string = [str(each) for each in list]
    for each in string:
        copyed_list.append(int(each))
    return copyed_list

def evolution(total_city_number,lists_number,lists,my_map):
    num = int(lists_number / 2)
    new_lists = []
    for i in range(0,num,2):
        old_list1 = copy_list(lists[i])
        old_list2 = copy_list(lists[i+1])
        judge1_old = my_distance(total_city_number,old_list1,my_map)
        judge2_old = my_distance(total_city_number,old_list2,my_map)
        new_list1,new_list2 = cross(total_city_number,lists[i],lists[i+1])
        random_variation = random.random()
        random_variation2 = random.random()
        if(random_variation<0.2):                #变异概率
            new_list1 = variation(total_city_number,new_list1)
        if (random_variation2 < 0.2):  # 变异概率
            new_list2 = variation(total_city_number, new_list2)
        judge1_new = my_distance(total_city_number, new_list1, my_map)
        judge2_new = my_distance(total_city_number, new_list2, my_map)
        if (judge1_new <= judge1_old):
            new_lists.append(new_list1)
        else:
            new_lists.append(old_list1)
        if (judge2_new <= judge2_old):
            new_lists.append(new_list2)
        else:
            new_lists.append(old_list2)
    for i in range(len(new_lists),lists_number):
        copyed = copy_list(lists[i])
        new_lists.append(variation(total_city_number,copyed))

    return lists_number,new_lists

tsp_file = 'data_51'
my_map, total_city_number = tsp_to_map(tsp_file)
lists_number, lists = initial(total_city_number)
min = 9999
min_list =[]
min_dai = 0
for dai in range(0,5000):
    print(dai)
    lists_number,lists = evolution(total_city_number,lists_number,lists,my_map)
    lists_number,lists,dis_lists = calculate_judge_of_each_generation(lists_number,total_city_number,lists)
    for list in lists:
        dis = my_distance(total_city_number,list,my_map)
        if(dis<min):
            min = dis
            min_list = list
            min_dai = dai
    # print("+++++++++++++++++++++++++++++++++++++++")
print("min",min,min_list)