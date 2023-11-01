# -*- coding:utf-8 -*-
import random
import numpy as np
from multiprocessing import Pool
from .mtsp_base import MtspBase,City
from .common import PltResult, TestCaseGenerate, PltProcess

class ACOMtsp(MtspBase):
    def __init__(self, cities:list[tuple], typeList:list[int], 
                 iters = 100, antsNum = 20, alpha = 1, beta = 2, rho = 0.8,
                 useMultiprocessing = False):
        """
        ACOMtsp.

        :param cities: city list e.g. [(0,0),(0,1)...]
        :param typeList: should be continue integers begin with 0  e.g.[0,1,2...n-1,n]
        """
        super().__init__(cities, typeList, iters)
        #初始化算法超参数
        self.antsNum = antsNum
        self.alpha = alpha
        self.beta = beta
        self.rho = rho

        #初始化缩放比例（防止城市之间距离过大或过小造成的影响)

        self.zoomRate = None

        #初始化启发矩阵和信息素矩阵
        self.heuristicMatrix = np.zeros(shape=(self.cityNum, self.cityNum), dtype=np.float64)
        self.pheromoneMartix = np.zeros(shape=(self.cityNum, self.cityNum), dtype=np.float64)

        #初始化蚁群轨迹列表和蚂蚁可访问城市类型列表
        self.types = set(range(self.typeNum))
        self.antPathList = None
        self.openGoalTypeList = None

        self.useMultiprocessing = useMultiprocessing
        if useMultiprocessing:
            self.pool = Pool()
    def chooseAction(self, antID:int):
        choiceList = []
        weightList = []
        startId = self.antPathList[antID][-1].id #上一次蚂蚁的位置
        for type in self.openGoalTypeList[antID]:
            for city in self.classifiedCityList[type]:
                choiceList.append(city)
                goalID = city.id
                weight = (self.pheromoneMartix[startId][goalID] ** self.alpha) \
                            * self.heuristicMatrix[startId][goalID]
                weightList.append(weight)
        choice = random.choices([0,1,2],[0.,0.1,0.9])[0] #0完全随机选 1选择最优 2按比重选择 
        if choice == 0 or sum(weightList) <= 0.0:
            res = random.choices(choiceList)[0]
        elif choice == 1:
            res = choiceList[weightList.index(max(weightList))]
        else:
            res = random.choices(choiceList , weightList)[0]
        return res
    # @profile
    def findPath(self):
        #初始化
        self.distanceMatrix = self.GetDistanceMartix()
        self.zoomRate = np.median(self.distanceMatrix)
        self.heuristicMatrix = 1 / ( ((self.distanceMatrix + 1e-3)/self.zoomRate) ** self.beta)

        #存储迭代过程
        historyBestValue = []
        #随机生成初始解
        bestSolution = []
        bestValue = None
        initValue = None

        for cities in self.classifiedCityList:
            bestSolution.append(random.choice(cities))
        initValue = bestValue = self.GetPathDistance(bestSolution)
        historyBestValue.append(bestValue)

        #使用随机解初始化信息素矩阵
        self.pheromoneMartix.fill( self.antsNum / (initValue/self.zoomRate) )

        #迭代开始
        for _ in range(self.iters):
            #初始化每只蚂蚁的路径和能到达的城市所售卖的商品类型
            self.antPathList = [[] for _ in range(self.antsNum)]
            self.openGoalTypeList = [self.types.copy() for _ in range(self.antsNum)]

            #为每一个蚂蚁选择出发点
            for i in range(self.antsNum):
                startCity = random.choice(self.cityList)
                self.antPathList[i].append(startCity)
                self.openGoalTypeList[i].remove(startCity.goodsType)

            #让蚂蚁开始行动！
            for _ in range(self.typeNum - 1): #选好出发点后，每个蚂蚁还能行动（typeNum - 1）步
                for i in range(self.antsNum):
                    nextCity = self.chooseAction(i) #为编号为i的蚂蚁选择行动
                    self.antPathList[i].append(nextCity)
                    self.openGoalTypeList[i].remove(nextCity.goodsType)

            #行动结束后更新信息素矩阵及全局最优解
            self.pheromoneMartix = self.pheromoneMartix * self.rho
            for i in range(self.antsNum):
                path = self.antPathList[i]
                pathValue = self.GetPathDistance(path)
                if pathValue < bestValue:
                    bestValue = pathValue
                    bestSolution = path
                
                for cityIndex in range(self.typeNum):
                    startCity = path[cityIndex]
                    goalCity = path[(cityIndex + 1) % self.typeNum]
                    self.pheromoneMartix[startCity.id][goalCity.id] += (1 - self.rho) *  (initValue / self.zoomRate)
                
                historyBestValue.append(bestValue)

            for cityIndex in range(self.typeNum):
                startCity = bestSolution[cityIndex]
                goalCity = bestSolution[(cityIndex + 1) % self.typeNum]
                self.pheromoneMartix[startCity.id][goalCity.id] += (1 - self.rho) *  (initValue / self.zoomRate)

        return bestSolution,bestValue,historyBestValue




if __name__ == '__main__': 
    cityPosList, goodsTypes = TestCaseGenerate(citynum = 100, typenum = 20, 
                                               scaleMax = 20, seed = seed)
    aco = ACOMtsp(cityPosList,goodsTypes)
    bestSolution, bestValue, historyBestValue = aco.findPath()

    print(bestSolution)
    print(bestValue)
    print([city.goodsType for city in bestSolution])
    ##### 显示收敛情况 #####
    PltProcess(historyBestValue)
    ##### 显示路线结果 #####
    PltResult(cityPosList, goodsTypes, [city.pos for city in bestSolution])