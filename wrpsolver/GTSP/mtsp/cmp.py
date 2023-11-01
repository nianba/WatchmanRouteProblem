import random
import numpy as np
from tabu_mtsp import TabuMtsp
from aco_mtsp import ACOMtsp
from common import PltResult, TestCaseGenerate, PltProcess
import time
seed = 0
random.seed(seed)
if __name__ == '__main__': 
    cityPosList, goodsTypes = TestCaseGenerate(citynum = 100, typenum = 20, 
                                               scaleMax = 200)
    time_tabu_begin = time.time()
    tabu = TabuMtsp(cityPosList,goodsTypes)
    bestSolution, bestValue, historyBestValues = tabu.findPath()
    print(bestSolution, bestValue)

    time_aco_begin = time.time()
    aco = ACOMtsp(cityPosList, goodsTypes)
    bestSolution, bestValue, historyBestValues = aco.findPath()
    print(bestSolution, bestValue)

    time_aco_end = time.time()
    print(time_aco_begin - time_tabu_begin, time_aco_end - time_aco_begin)