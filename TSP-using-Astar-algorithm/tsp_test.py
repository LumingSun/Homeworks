from my_list import close_list
from distance import my_distance
from choose_a_way import choose_f_min
from dist_map import tsp_to_map
from choose_a_way import name_of_means
import time
start_time = time.time()
class Node:
    def __init__(self):
        self.No = 0
        self.open = 0   #0 not in, 1 in
        self.close = 0  #0 not in, 1 in
        self.father = 0
        self.F = 0
        self.G = 0
        self.H =0
        self.depth = 0  #在路径中的第几个点 1:51

def tsp_test(input_file,output_file,means):
    (my_map, total_city_number,max_in_map,min_in_map) = tsp_to_map(input_file,output_file)
    cities = []                            #cities是所有点的数据结构
    now_node = 0
    result = [1]
    #print(max_in_map,min_in_map)
    # cities.No从0开始！！！              #初始化表
    for i in range(0, total_city_number):
        cities.append(Node())
        cities[i].No = i
        cities[i].G = my_map[i][0]
        #print(cities[i].No,cities[i].G)
    cities[0].close = 1

    while(close_list(total_city_number,cities) != total_city_number):
        next_node = choose_f_min(total_city_number,now_node,cities,my_map,means,max_in_map,min_in_map)
        result.append(next_node+1)
        cities[next_node].close = 1
        cities[next_node].father = now_node
        now_node = next_node
    cities[0].father = now_node
    '''for i in range(0,total_city_number):
        print(cities[i].No,cities[i].father)                #输出各个节点的序号及其父节点序号
    r = {}
    for i in range(0,total_city_number):                    #将节点和其父节点存为字典
        r[i]=cities[i].father'''
    print("my result:",result)
    dis = my_distance(total_city_number,result,my_map)
    print("my distance:",dis)
    # best_list =[1,22,8,26,31,28,3,36,35,20,2,29,21,16,50,34,30,9,49,10,39,33,45,15,44,42,40,19,41,13,25,14,24,43,7,23,48,6,27,51,46,12,47,18,4,17,37,5,38,11,32,0]
    # dis = my_distance(total_city_number,best_list,my_map)
    # print("best list",best_list)
    # print("best way",dis)
for i in range(1,10):
    print("solving tsp using way", name_of_means(i))
    tsp_test(r'G:\\python\\tsp\TSP-using-Astar-algorithm\data_318', "G:\\python\\tsp\TSP-using-Astar-algorithm\map.txt",i)
    print("-------------------------------------------------------------------------------------------------------------")
print("总共耗时（秒）：" + str(time.time() - start_time))

