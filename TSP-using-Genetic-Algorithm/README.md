##  solving tsp problem using genetic algorithm
##  使用遗传算法解决tsp问题
#### 本次实验代码已上传至github：https://github.com/LumingSun/TSP-using-Genetic-Algorithm
### 1.输入数据格式
第一列为节点序号，二三列为节点坐标。
   1 37 52  
    2 49 49  
    ......  
    50 56 37  
    51 30 40  
### 2.输出
    输出循环的代数和算法得到的最短路径以及该路径的节点顺序。

### 3.算法说明
    tsp_to_map() 与Astar算法中的函数功能相同，将输入的文件转换为距离矩阵。
    initial() 用于产生初始的种群，可以定义初始种群的个数，返回n个随机序列。
    my_distance() 作为遗传算法中的judge因素，将某一序列的距离作为判断其能否生存下去的选择因素。
    cross() 将输入的两个个体序列进行交叉，实现的方式是：随机选取某两个序列长度内的数作为交叉基因的start和end，
            将这两个序列[start:end]之间的节点互换，完成交叉。为了避免节点重复，再逐个将没有交叉部分的节点和交叉
            后部分的进行替换，最终使序列经过所有城市一次。
    variation() 用于实现个体的变异，随机产生两个数，将这两个数位置上的节点互换。完成变异。
    calculate_judge_of_each_generation() 计算一代种群的生存率（即距离），并将种群个体按照距离从小到大排序后返回。
    copy_list() 将一个list复制，稍后将具体说明为什么需要这个函数。
    evolution() 进化算法，在我的算法中，我采用了这样的策略：每一代个体按照生存率从大到小排序后，对种群中的前一半个体，
                每两个为一组，进行交叉，得到两个新的个体，新的个体按照0.2的概率进行变异，然后如果新个体的生存率大于原个体，
                则将新个体加入新种群，否则，仍然将老个体加入新种群。这样的方式保证了交叉产生的前一半新种群的生存率总是大于
                或等于原来的种群。对于种群中的后一半个体，对他们分别进行变异，再加入新种群。
    在主函数中，每代进行一次evolution()，并计算judge_of_each_generation，迭代指定的代数。
   
 
### 4.测试结果
51个节点，初始种群数量为51 * 10=510，遗传代数为5000，一次实验，取得的最优解是475.407719837  
最优解时的顺序为： [2, 22, 27, 32, 11, 38, 5, 49, 10, 15, 37, 17, 4, 47, 12, 46, 0, 48, 6, 18, 14, 25, 13, 41, 40, 19, 42, 44, 45, 33, 39, 30, 34, 50, 9, 16, 21, 29, 20, 35, 36, 3, 28, 31, 23, 24, 43, 7, 26, 8, 1]  
51个节点，初始种群数量为51 * 10=510，遗传代数为50000，一次实验，取得的最优解是429.098067846   
这个解与老师给出的最优解426已经非常接近。另一次同样参数的结果是454.33652028，也比Astar算法结果更好。  
最优解时的顺序为：[22, 2, 16, 50, 9, 38, 5, 37, 17, 4, 18, 47, 12, 0, 46, 11, 32, 27, 6, 48, 23, 7, 43, 24, 14, 25, 13, 41, 40, 19, 42, 44, 15, 45, 33, 39, 10, 49, 30, 34, 21, 29, 20, 35, 36, 3, 28, 31,   26, 8, 1]  
318个节点，初始种群数量为381，遗传代数为50000，一次实验，取得的最优解是142058.69059，另一次实验，取得的结果是136917.279467
最优解时的顺序为：[169, 210, 164, 153, 42, 52, 39, 38, 166, 165, 259, 255, 149, 158, 167, 186, 88, 201, 202, 184, 203, 204, 194, 179, 163, 146, 151, 144, 250, 258, 260, 261, 272, 283, 273, 286, 145, 152, 132, 122, 225, 232, 119, 221, 222, 140, 26, 18, 34, 35, 53, 63, 62, 136, 135, 137, 118, 213, 218, 235, 228, 236, 254, 256, 264, 315, 269, 157, 209, 159, 162, 295, 288, 246, 243, 241, 139, 143, 148, 147, 120, 208, 141, 142, 160, 176, 183, 190, 43, 37, 33, 16, 36, 15, 20, 28, 41, 191, 198, 199, 278, 220, 211, 216, 212, 17, 24, 40, 316, 317, 56, 50, 104, 51, 189, 181, 195, 193, 292, 293, 294, 289, 290, 251, 253, 237, 234, 227, 226, 229, 314, 168, 44, 46, 174, 185, 175, 287, 296, 301, 302, 180, 177, 182, 87, 81, 161, 156, 127, 134, 138, 130, 242, 240, 247, 219, 230, 239, 231, 109, 110, 108, 112, 14, 116, 117, 121, 124, 129, 131, 123, 313, 233, 238, 224, 245, 266, 192, 200, 207, 206, 100, 94, 95, 99, 98, 89, 75, 74, 73, 80, 90, 196, 197, 282, 284, 279, 291, 285, 280, 274, 277, 281, 170, 171, 154, 47, 55, 105, 59, 70, 69, 60, 65, 188, 173, 66, 58, 54, 57, 48, 45, 49, 32, 29, 22, 11, 10, 12, 19, 115, 133, 125, 128, 126, 150, 155, 61, 187, 172, 178, 270, 271, 0, 262, 252, 257, 267, 248, 263, 268, 265, 13, 103, 21, 7, 6, 2, 30, 31, 23, 27, 111, 113, 114, 106, 107, 5, 4, 9, 8, 25, 71, 83, 82, 78, 91, 101, 102, 97, 96, 92, 93, 86, 84, 77, 79, 72, 64, 67, 68, 85, 76, 298, 297, 310, 304, 305, 309, 308, 306, 307, 205, 312, 311, 303, 300, 299, 276, 275, 249, 244, 223, 215, 214, 217, 3, 1]

### 5.小结
    对于51个结点的tsp问题，遗传算法的效果比Astar算法得到的效果更好，但是耗时较久。
    对于318个结点的tsp问题，遗传算法耗时久，且效果不如astar算法的最有结果，目前正在将遗传代数增加，在实验室集群上跑，以求更好的结果。
### 6.遇到的坑
    1.list of list:
        list = [[1,2,3],[4,5,6],[7,8,9]]
        new = list[1]
        print(new)
        list[1]=[0,0,0]
        print(new)
        
        output:[4,5,6]
               [4,5,6]
    开始这个问题困扰我很久，对于一个元素是列表的列表，列表的复制不能简单的用 = ，这貌似是因为python是用指针来完成对列表的赋值的，
    所以列表修改，新列表也会跟着变化。这也是定义了copy_list函数的原因。   
    2.dictionary
    没有注意到这个问题时，经常发生下一代的种群数量小于上一代的情况，找了好久，发现开始我在求每代的distance时，使用的字典的数据格式
    存储的列表序列和生存率，但由于进化算法中，可能存在同样的序列（即个体），而字典类型对于重复的key只存储一次，所以造成了种群数量
    不断减少的情况，再修改代码之后，得到了解决。