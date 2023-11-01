import shapely
import math
from shapely.ops import split
from ..Global import *

def GetKernel(polygon, watcher):

    kernel = polygon
    reflexPointList = []
    pointList = list(polygon.exterior.coords)
    pointList.pop()  # 去除重复顶点
    pointList.reverse()  # 去除重复顶点
    ring = shapely.LinearRing(pointList)
    ccw = ring.is_ccw
    # 模拟循环链表
    n = pointNum = len(pointList)
    while pointNum < 2 * n:
        point = pointList[(pointNum) % n]
        pointLeft = pointList[(pointNum - 1) % n]
        pointRight = pointList[(pointNum + 1) % n]
        rayLine = GetRayLine(point, pointRight)
        splitedPolygons = split(kernel, rayLine)
        isConvex = (((point[0] - pointLeft[0]) * (pointRight[1] - pointLeft[1]) -
                    (pointRight[0] - pointLeft[0]) * (point[1] - pointLeft[1])) < 0)
        if (isConvex ^ (not ccw)):
            reflexPointList.append(point)
        for p in list(splitedPolygons.geoms):
            if p.intersects(watcher):
                kernel = p
                break

        pointNum += 1
    return kernel, reflexPointList


def GetRayLine(watcher, vertex):
    xGap = vertex[0] - watcher[0]
    yGap = vertex[1] - watcher[1]
    rate = (pic_size/(math.hypot(xGap, yGap)))*100000
    extendPoint1 = (watcher[0] + xGap*rate,watcher[1] + yGap*rate)
    extendPoint2 = (watcher[0] - xGap*rate,watcher[1] - yGap*rate)
    return shapely.LineString([extendPoint1, extendPoint2])


# def 