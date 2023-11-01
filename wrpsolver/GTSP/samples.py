import shapely
import math
import random
import numpy as np

def getLineList(lines):
    lineList = []
    if (type(lines) == shapely.LineString or type(lines) == shapely.LinearRing):
        lineList.append(lines)
    elif (type(lines) == shapely.MultiLineString):
        for line in lines.geoms:
            lineList.append(line)
    return lineList


def GetSample(polygonList, polygon, dSample, gridMap, step = 3):

    sampleList = []
    freeSpace = polygon.buffer(-1, join_style=2)
    obstacle = polygon.boundary.buffer(1,join_style=2)
    for polygon in polygonList:
        pointList = []
        tempPointList = []
        lineList = getLineList(polygon.boundary.difference(obstacle))
        for line in lineList:
            if line.length < 2:
                continue
            path = dSample
            while (path < line.length):
                point = shapely.line_interpolate_point(line, path)
                if freeSpace.contains(point):
                    tempPointList.append(point)
                path += dSample
            start = shapely.line_interpolate_point(line, 1)
            if freeSpace.contains(start):
                tempPointList.append(start)
        for point in tempPointList:
            x1 = math.ceil(point.x/step) * step
            x2 = x1 - step
            y1 = math.ceil(point.y/step) * step
            y2 = y1 - step
            candidates = [(x1,y1),(x1,y2),(x2,y1),(x2,y2)]
            random.shuffle ( candidates )
            for pos in candidates:
                if pos[1] < gridMap.shape[0] and pos[0] < gridMap.shape[1] and gridMap[pos[1]][pos[0]] != 0:
                    pointList.append(pos)
                    break
                    
        pointList = list(dict.fromkeys(pointList))  # 去重
        if (len(pointList) > 0):
            sampleList.append(pointList)
    return sampleList


def postProcessing(sampleList):
    cityPos = []
    cityGoods = []
    cityClass = []
    n = 0
    for sample in sampleList:
        classify = []
        for point in sample:
            cityPos.append((point[0], point[1]))
            cityGoods.append(sampleList.index(sample))
            classify.append(n)
            n += 1
        if (len(classify) > 0):
            cityClass.append(classify)
    # for i in range(len(cityPos)):
    #     x = cityPos[i][0]
    #     y = cityPos[i][1]
    #     x = np.round(x).astype(np.int32)
    #     y = np.round(y).astype(np.int32)
    #     cityPos[i] = (x,y)
    return ((cityPos, cityGoods, cityClass))


