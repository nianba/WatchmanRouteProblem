import math
import numpy as np
from abc import ABC, abstractmethod

class City():
    def __init__(self, id:int, pos:tuple, goodsType:int):
        self.id = id
        self.pos = pos
        self.goodsType = goodsType
    
    def __eq__(self, __value: object) -> bool:
        if self.pos == __value.pos:
            return True
        return False
    def __ne__(self, __value: object) -> bool:
        # if self.id != __value.id or self.pos != __value.pos:
        if self.pos != __value.pos:
            return True
        return False
    def __str__(self):
        return str(self.pos)
    def __repr__(self):
        return str(self.pos)
    
class MtspBase(ABC):
    def __init__(self, cities:list[tuple], typeList:list[int], iters = 1000):
        """
        MtspBase.

        :param cities: city list e.g. [(0,0),(0,1)...]
        :param typeList: should be continue integers begin with 0  e.g.[0,1,2...n-1,n]
        """
        #初始化城市数量
        self.cityNum = len(cities)
        self.typeNum = max(typeList) + 1
        assert self.typeNum >= 1 and self.cityNum >= 2 and len(cities) == len(typeList)

        #初始化城市列表
        self.cities = cities
        self.cityList = []
        for i in range(self.cityNum):
            city = City(i,cities[i],typeList[i])
            self.cityList.append(city)

        #初始化类别城市列表
        classifiedCityList = [ [] for _ in range(self.typeNum) ]
        for city in self.cityList:
            classifiedCityList[city.goodsType].append(city)
        self.classifiedCityList = classifiedCityList

        #初始化城市之间的距离矩阵
        self.distanceMatrix = None
        
        #初始化算法超参数
        self.iters = iters

        
    def GetDistanceMartix(self):
        distanceMatrix = np.zeros(shape=(self.cityNum, self.cityNum), dtype=np.float64)
        for i in range(self.cityNum):
            for j in range(self.cityNum):
                #默认 "a->b" 与 "b->a" 的距离相等
                if j < i:
                    distanceMatrix[i][j] = distanceMatrix[j][i]
                elif j == i:
                    distanceMatrix[i][j] = float('inf')
                else:
                    distanceMatrix[i][j] = self.GetDistanceBetween(self.cityList[i],self.cityList[j])
        return distanceMatrix

    def GetDistanceBetween(self, city1, city2):
        #本次实验采用两个城市之间的欧式距离
        (x1,y1) = city1.pos
        (x2,y2) = city2.pos
        return math.hypot(x2 - x1, y2 - y1)
    
    def GetPathDistance(self, path:list):
        result = 0
        n = len(path)
        for i in range(0, n-1):
            start = path[i]
            goal = path[((i+1)%n)]
            result += self.distanceMatrix[start.id][goal.id]
        return result
    
    @abstractmethod
    def findPath(self):
        assert False