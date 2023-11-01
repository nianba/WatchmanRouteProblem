import numpy as np
import random
import logging
from multiprocessing import Pool,Manager
from .astar.a_star import findPath
from .mtsp.tabu_mtsp import TabuMtsp
from .mtsp.aco_mtsp import ACOMtsp

class TabuMtspAstar(TabuMtsp):
    def __init__(self, cities:list[tuple], typeList:list[int], iters = 1000, 
                 tabuLimit = 10, maxCandidateNum = None, choice = 0.8,
                 grid = None):
        super().__init__(cities,typeList,iters,max(typeList),maxCandidateNum,choice)
        self.path = None
        self.grid = grid

    def GetDistanceMartix(self):
        path, distance = RecordDistance(self.cities, self.grid, self.cityNum)
        self.path = path
        return distance
class ACOMtspAstar(ACOMtsp):
    def __init__(self, cities:list[tuple], typeList:list[int], iters = 100, 
                 antsNum = 40, alpha = 1, beta = 2, rho = 0.8,
                 grid = None):
        super().__init__(cities, typeList, iters, antsNum, alpha, beta, rho)
        self.path = None
        self.grid = grid

    def GetDistanceMartix(self):
        path, distance = RecordDistance(self.cities, self.grid, self.cityNum)
        self.path = path
        return distance


def ColisionFreeDistance(args):#多线程求无碰撞距离
    i = args[0]
    city_position = args[1]
    paths = args[2]
    distances = args[3]
    grid = args[4]
    num = len(city_position)  # 城市数量
    logging.debug(i)
    for j in range(i,num):
        path, distance = findPath(
            (city_position[i][0], city_position[i][1]), (city_position[j][0], city_position[j][1]),grid)

        distances.append(distance)
        paths.append(path)

def RecordDistance(city_position, grid, num):
    manager = Manager()
    tempPaths = [manager.list() for _ in range(num)]
    tempDistances = [manager.list() for _ in range(num)]
    for i in range(num):
        for j in range(i):
            tempPaths[i].append(0)
            tempDistances[i].append(0)
    pool = Pool(12)

    pool.map(ColisionFreeDistance,iterable = [(i,city_position,tempPaths[i],tempDistances[i],grid) for i in range(num)])
    pool.close()
    pool.join()
    paths = np.eye(num, dtype=object)
    distances = np.eye(num)
    for i in range(num):
        for j in range(i,num):
            paths[i][j]  = tempPaths[i][j]
            paths[j][i] = paths[i][j].copy()
            paths[j][i].reverse()
            distances[i][j] = distances[j][i] = tempDistances[i][j]
    return paths, distances


def cal_cost(distance, solution, goods_num):
    cost = 0
    for j in range(goods_num-1):
        cost += distance[solution[j]][solution[j+1]]
    return cost

def GetTraceTabu(tspCase, grid):
    cityPosList, goodsTypes, _ = tspCase
    mtspSolver = TabuMtspAstar(cityPosList,goodsTypes,grid = grid)
    bestSolution, bestValue, _ = mtspSolver.findPath()
    solutionID = [ city.id  for city in bestSolution]

    solution = [city.pos for city in bestSolution]
    path = [mtspSolver.path[solutionID[i]][solutionID[i+1]]
            for i in range(len(solution)-1)]
    return solution, bestValue, path

def GetTraceACO(tspCase, grid):
    cityPosList, goodsTypes, _ = tspCase
    mtspSolver = ACOMtspAstar(cityPosList,goodsTypes,grid = grid)
    bestSolution, bestValue, _ = mtspSolver.findPath()
    solutionID = [ city.id  for city in bestSolution]

    solution = [city.pos for city in bestSolution]
    path = [mtspSolver.path[solutionID[i]][solutionID[i+1]]
            for i in range(len(solution)-1)]
    return solution, bestValue, path


def GetTrace(tspCase, grid):
    ##### 参数及相关数据初始化 #####
    # 初始化城市实例
    city_position, goods_class, city_class = tspCase
    city_num = len(city_position)             # 城市数目
    goods_num = len(set(goods_class))         # 商品种类数目
    path, distance = RecordDistance(city_position, grid, city_num)  # 得到距离矩阵

    iter_num = 1000       # 迭代次数
    tabu_list = []        # 禁忌表
    tabu_time = []        # 禁忌时间表
    current_tabu_num = 0  # 当前禁忌对象数量
    tabu_limit = goods_num       # 特赦规则(50次)

    # 候选集
    candidate_num = city_num
    candidate = []
    candidate_value = []

    ##### 生成随机初始解 #####
    current_solution = []
    for x in city_class:
        current_solution.append(x[random.randrange(len(x))])
    random.shuffle(current_solution)

    current_value = [cal_cost(distance, current_solution, goods_num)]  # 计算价值

    best_solution = current_solution.copy()  # 最优路径
    bestvalue = current_value[-1]           # 最优值
    best_value = [bestvalue]  # 记录迭代过程中的最优解

    ##### 开始迭代 #####
    for i in range(iter_num):
        ##### 得到邻域 候选解 #####
        # 初始化本轮候选集
        candidate = []
        candidate_value = []
        temp = 0
        stepCnt = 0
        # 随机选取邻域
        while True:
            # 从邻域选择新解 - 同一类城市交换 + 现有的两交换
            seed = np.random.rand()
            if seed > 0.8:  # 随机交换卖同一类商品城市的两个节点
                goods = random.randrange(goods_num)
                if len(city_class[goods]) == 1:
                    continue
                for index, city in enumerate(city_class[goods]):
                    if city in current_solution:
                        loc = current_solution.index(city)
                        while True:
                            tmp = random.randrange(len(city_class[goods]))
                            if tmp != index:
                                break
                        candidate.append(current_solution.copy())
                        candidate[temp][loc] = city_class[goods][tmp]
            else:  # 交换两个城市
                current = random.sample(range(0, goods_num), 2)
                candidate.append(current_solution.copy())
                candidate[temp][current[0]], candidate[temp][current[1]
                                                             ] = candidate[temp][current[1]], candidate[temp][current[0]]  # 交换

            if len(candidate) == temp:
                continue
            # 若不在禁忌表中则放入候选集
            if (candidate[temp] not in tabu_list) or stepCnt>100000:
                candidate_value.append(
                    cal_cost(distance, candidate[temp], goods_num))
                temp += 1
            else:
                candidate.pop()
            if temp >= candidate_num:
                break
            stepCnt += 1

        # 得到候选解中的最优解

        candidate_best = min(candidate_value)
        best_index = candidate_value.index(candidate_best)

        current_value.append(candidate_best)
        current_solution = candidate[best_index].copy()

        # 与当前最优解进行比较
        if current_value[-1] < bestvalue:
            best_value.append(current_value[-1])
            bestvalue = current_value[-1]
            best_solution = current_solution.copy()
        else:
            best_value.append(best_value[-1])

        # 将最优的加入禁忌表
        tabu_list.append(candidate[best_index])
        tabu_time.append(tabu_limit)
        current_tabu_num += 1

        ##### 更新禁忌表以及禁忌期限 #####
        del_num = 0
        temp = [0 for col in range(goods_num)]
        # 更新步长
        tabu_time = [x-1 for x in tabu_time]
        # 如果达到期限，释放
        for i in range(current_tabu_num):
            if tabu_time[i] == 0:
                del_num += 1
                tabu_list.pop(i)

        current_tabu_num -= del_num
        while 0 in tabu_time:
            tabu_time.remove(0)

    solution = [city_position[i] for i in best_solution]
    path = [path[best_solution[i]][best_solution[(i+1)%(len(best_solution))]]
            for i in range(len(best_solution)-1)]
    return solution, bestvalue, path
