def tsp_to_map(input_file,output_file):
    import numpy as np
    import math
    data = open(input_file)
    i = 0
    ID =[]
    xcoor = []
    ycoor = []
    for line in data:
        line = line.replace('\n', '')
        line = (line.split(" "))
        ID.append(int(line[0]))
        xcoor.append(float(line[1]))
        ycoor.append(float(line[2]))
        i = i+1
    #print("number of cities:",i)
    dist_map = np.zeros((i,i))
    min_in_map = 9999999999
    max_in_map = 0
    for m in range(0,i):
        for n in range(0,i):
            dist_map[m][n] = math.sqrt(math.pow(xcoor[m]-xcoor[n],2)+math.pow(ycoor[m]-ycoor[n],2))
            if(dist_map[m][m] < min_in_map and dist_map[m][n] != 0):
                min_in_map = dist_map[m][n]
            if(dist_map[m][n] > max_in_map):
                max_in_map = dist_map[m][n]
    np.savetxt(output_file,dist_map)
    return dist_map,i,max_in_map,min_in_map








