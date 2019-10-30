def my_distance(total_city_number,result_list,my_map):
    dis = 0
    for i in range(0,total_city_number-1):
        dis = dis + my_map[result_list[i]-1][result_list[i+1]-1]
    #print(total_city_number)
    #print(my_map[result_list[total_city_number - 1]-1][0])
    dis = dis + my_map[result_list[total_city_number - 1]-1][0]
    return dis