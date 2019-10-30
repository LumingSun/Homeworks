def close_list(total_city_num,cities):
    close_list = []
    number = 0
    for i in range(0,total_city_num):
        if(cities[i].close == 1):
            number = number + 1
            close_list.append(i)
    return number #,close_list


def open_list(total_city_num,cities):
    open_list = []
    number = 0
    for i in range(0,total_city_num):
        if(cities[i].open == 1):
            number = number + 1
            open_list.append(i)
    return number,open_list

