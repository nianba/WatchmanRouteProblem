# -*- coding:utf-8 -*-
# author: xkey
# 禁忌搜索
# 邻域 邻域动作 禁忌表 候选集合 评价函数 特赦规则
import random
import numpy as np
from .mtsp_base import MtspBase,City
from .common import PltResult, TestCaseGenerate, PltProcess
class TabuMtsp(MtspBase):
    def __init__(self, cities:list[tuple], typeList:list[int], 
                 iters = 1000, tabuLimit = 50, maxCandidateNum = None, choice = 0.8):
        """
        TabuMtsp.

        :param cities: city list e.g. [(0,0),(0,1)...]
        :param typeList: should be continue integers begin with 0  e.g.[0,1,2...n-1,n]
        """
        super().__init__(cities, typeList, iters)
        #初始化算法超参数
        self.tabuLimit = tabuLimit
        self.maxCandidateNum = maxCandidateNum
        if maxCandidateNum == None:
            self.maxCandidateNum = self.cityNum
        self.choice = choice

    def sampleNeighbor(self, path:list):
        result = path.copy()
        nodeIndex = random.randint(0, len(path)-1)
        node = path[nodeIndex]

        seed = np.random.rand()
        if seed > self.choice and len(self.classifiedCityList[node.goodsType]) > 1: #交换售卖同种商品的不同城市
            for city in self.classifiedCityList[node.goodsType]:
                if city.id != node.id:
                    result[nodeIndex] = city
                    break
        else:
            node2Index = random.randint(0, len(path)-1) #交换不同城市的访问顺序
            while node2Index == nodeIndex:
                node2Index = random.randint(0, len(path)-1)
            result[nodeIndex], result[node2Index] = result[node2Index], result[nodeIndex]
            
        return result

    def findPath(self):
        #初始化距离矩阵
        self.distanceMatrix = self.GetDistanceMartix()

        #初始化禁忌表和禁忌时间表
        tabuList = []
        tabuTimeList = []


        #随机生成初始解
        currentSolution = []
        for cities in self.classifiedCityList:
            currentSolution.append(random.choice(cities))
        random.shuffle(currentSolution)
        
        #初始解设定为最优解
        bestSolution = currentSolution.copy()
        bestValue = self.GetPathDistance(bestSolution)
        historyBestValues = [bestValue] #用于优化过程图

        #迭代开始
        for _ in range(self.iters):
            candidateList = []
            candidateValueList = []
            candidateCnt = 0
            repeatCnt = 0
            while(candidateCnt < self.maxCandidateNum):
                neighbor = self.sampleNeighbor(currentSolution)
                if neighbor not in tabuList:
                    candidateList.append(neighbor)
                    candidateValueList.append(self.GetPathDistance(neighbor))
                    candidateCnt += 1
                else:
                    repeatCnt += 1
                if repeatCnt > 1000:
                    break
            if len(candidateList) == 0:
                continue
            bestCandidateValue = min(candidateValueList)
            bestCandidateIndex = candidateValueList.index(bestCandidateValue)
            currentSolution = candidateList[bestCandidateIndex].copy()
            
            # 与当前最优解进行比较 
            if bestCandidateValue < bestValue:
                bestValue = bestCandidateValue
                bestSolution = candidateList[bestCandidateIndex].copy()
                historyBestValues.append(bestCandidateValue)
            else:
                historyBestValues.append(historyBestValues[-1])
            
            # 将最优的加入禁忌表
            tabuList.append(candidateList[bestCandidateIndex])

            tabuTimeList.append(self.tabuLimit)

            #更新禁忌表
            tabuTimeList = [time-1 for time in tabuTimeList]
            # 如果达到期限，释放
            for i in range(len(tabuList)):
                if tabuTimeList[i] == 0:
                    tabuList.pop(i)
            while 0 in tabuTimeList:
                tabuTimeList.remove(0)

        return bestSolution, bestValue, historyBestValues

if __name__ == '__main__': 
    cityPosList, goodsTypes = TestCaseGenerate(citynum = 100, typenum = 20, 
                                               scaleMax = 20, seed = seed)
    tabu = TabuMtsp(cityPosList,goodsTypes)
    bestSolution, bestValue, historyBestValues = tabu.findPath()

    print(bestSolution, bestValue)
    ##### 显示收敛情况 #####
    PltProcess(historyBestValues)
    ##### 显示路线结果 #####
    PltResult(cityPosList, goodsTypes, [city.pos for city in bestSolution])