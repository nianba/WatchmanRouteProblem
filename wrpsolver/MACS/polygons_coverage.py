#!/usr/bin/python3.8
# -*- coding:utf-8 -*-
import shapely
import random
import math
from shapely.ops import split, nearest_points
from multiprocessing import Pool

from .compute_kernel import GetKernel
from .compute_visibility import GetVisibilityPolygon
from ..Global import *
from ..Test.draw_pictures import *
def SelectMaxPolygon(polygons):
    MaxPolygon = None
    if polygons is None:
        print("polygons is None")
        return None
    elif (type(polygons) == shapely.Polygon):
        MaxPolygon = polygons
    else:
        for p in list(polygons.geoms):
            if (type(p) == shapely.MultiPolygon) or (type(p) == shapely.GeometryCollection):
                p = SelectMaxPolygon(p)
            elif MaxPolygon == None or ((type(p) == shapely.Polygon) and p.area > MaxPolygon.area):
                MaxPolygon = p
    if(MaxPolygon) == None:
        print("SelectMaxPolygon Failed",type(polygons))
    return MaxPolygon


def SelectPointFromPolygon(polygon):
    minx, miny, maxx, maxy = polygon.bounds
    tempPolygon = polygon.buffer(-1)
    while True:
        p = shapely.Point(random.uniform(minx, maxx),
                          random.uniform(miny, maxy))
        if tempPolygon.contains(p):
            return p
def FindVisibleRegion(polygon, watcher, d = 32, useCPP = False):

    visiblePolygon = GetVisibilityPolygon(polygon, watcher)

    dVisibility = watcher.buffer(d)  # d范围视距
    visiblePolygon = visiblePolygon.intersection(dVisibility)  # 有限视距下的可视范围

    visiblePolygon = SelectMaxPolygon(visiblePolygon)
    if(visiblePolygon == None):
        print("failed find visibile polygon")

    return visiblePolygon.simplify(1, preserve_topology=False)




def GetKernelPolygon(visiblePolygon):
    xList, yList = GetKernel(visiblePolygon)
    kernel = list(zip(xList, yList))
    return shapely.Polygon(kernel)


def GetRayLine(watcher, vertex):
    xGap = vertex[0] - watcher[0]
    yGap = vertex[1] - watcher[1]
    rate = (pic_size/(math.hypot(xGap, yGap)))*100000
    if (rate < 100):
        # print(rate,xGap,yGap,vertex)
        pass
    extendPoint1 = (watcher[0] + xGap*rate,watcher[1] + yGap*rate)
    extendPoint2 = (watcher[0] - xGap*rate,watcher[1] - yGap*rate)
    return shapely.LineString([extendPoint1, extendPoint2])


def GetSingleReflexChord(visiblePolygonPointList, reflexPoint, kernel):

    prependicular = None
    kernelPointList = list(kernel.exterior.coords)
    kernelPointList.pop()
    kernelPointList.reverse()
    if (reflexPoint in list(kernelPointList)):  # 如果反射点在kernel上
        numOfKernelPoints = len(kernelPointList)
        reflex_kernel_pos = visiblePolygonPointList.index(reflexPoint)
        reflexKernelLeft = kernelPointList[(reflex_kernel_pos - 1) % numOfKernelPoints]
        reflexKernelRight = kernelPointList[(reflex_kernel_pos + 1) % numOfKernelPoints]
        # 和弦的斜率应为 反射点临边斜率的平均值
        if (abs(reflexPoint[0] - reflexKernelLeft[0]) < 1e-2 or abs(reflexKernelRight[0] - reflexPoint[0]) < 1e-2):
            extendPoint = (reflexPoint[0], reflexPoint[1] + 1)
        else:
            prependicular1 = (reflexKernelRight[1] - reflexPoint[1]) / (reflexKernelRight[0] - reflexPoint[0])
            prependicular2 = (reflexPoint[1] - reflexKernelLeft[1]) / (reflexPoint[0] - reflexKernelLeft[0])

            prependicular = (prependicular1 + prependicular2) / 2
            extendPoint = (reflexPoint[0]+1, reflexPoint[1] + prependicular)
    else:
        point = shapely.Point(reflexPoint)  # 如果反射点不在kernel上
        nearestPoint = (nearest_points(point, kernel))[1]
        # 和弦的斜率应为 点连线的垂线的斜率
        if abs(point.y - nearestPoint.y) < 1e-6:  # 斜率判断
            extendPoint = (reflexPoint[0], reflexPoint[1] + 1)

        else:
            prependicular = (nearestPoint.x - point.x) / (point.y - nearestPoint.y)
            extendPoint = (reflexPoint[0]+1, reflexPoint[1] + prependicular)
    return GetRayLine(reflexPoint, extendPoint)

def GetSplitedPolygon(chord, visiblePolygon, watcher):
    polygon = shapely.Point(1,1)
    tempVisiblePolygon = visiblePolygon
    polygons = list(split(tempVisiblePolygon, chord).geoms)
    for polygon in polygons:
        if type(polygon) == (shapely.Polygon) and polygon.contains(watcher):
            return polygon
    # print(polygons)
    return polygon

def MaximallyCoveringConvexSubset(args):  # MCCS
    unCoveredPolygon = args[0]
    initialPolygon = args[1]
    watcher = args[2]
    d = args[3]
    visiblePolygon = FindVisibleRegion(
        initialPolygon, watcher, d,False)  # d为可视距离

    kernelPolygon, reflexPointList = GetKernel(visiblePolygon, watcher)
    reflexPointList.sort(key=lambda watcher: shapely.distance(
        kernelPolygon, shapely.Point(watcher)))  # 列表排序
    polygon = visiblePolygon
    numOfReflexPoints = len(reflexPointList)
    ###
    # image = np.zeros((1000, 1000, 3), dtype=np.uint8)
    # DrawPolygon( list(initialPolygon.exterior.coords), (255, 255, 255), image, zoomRate=10)
    # DrawPolygon( list(visiblePolygon.exterior.coords), (0, 255, 255), image, zoomRate=10)
    # DrawPolygon( list(kernelPolygon.exterior.coords), (0, 0, 255), image, zoomRate=10)
    # DrawPoints(image, watcher.x, watcher.y,zoomRate=(10))
    # for p in reflexPointList:
    #     DrawPoints(image, p[0], p[1],size= 3,zoomRate=(10))
    # cv2.imwrite('test.png',image)
    # exit()

    ###

    for i in range(numOfReflexPoints):

        polygonPointList = list(polygon.exterior.coords)
        polygonPointList.pop()
        numOfPolygonPoints = len(polygonPointList)
        reflexPoint1 = reflexPointList[i]
        reflexPoint2 = reflexPointList[(i+1) % numOfReflexPoints]

        if (reflexPoint1 not in polygonPointList):
            continue
        r1Pos = polygonPointList.index(reflexPoint1)
        r1Left = polygonPointList[(r1Pos - 1) % numOfPolygonPoints]
        r1Right = polygonPointList[(r1Pos + 1) % numOfPolygonPoints]

        # extremal chords
        chord = GetRayLine(reflexPoint1, r1Left)
        ePolygon1 = GetSplitedPolygon(chord, polygon, watcher)

        chord = GetRayLine(reflexPoint1, r1Right)
        ePolygon2 = GetSplitedPolygon(chord, polygon, watcher)

        # two reflex chord
        if (len(reflexPointList) > 1):
            chord = GetRayLine(reflexPoint1, reflexPoint2)
            tPolygon = GetSplitedPolygon(chord, polygon, watcher)
        else:
            tPolygon = shapely.Point(1, 1)  # area of point is 0

        # single reflex chord
        chord = GetSingleReflexChord(
            polygonPointList, reflexPoint1, kernelPolygon)
        sPolygon = GetSplitedPolygon(chord, polygon, watcher)
        polygon = max(ePolygon1, ePolygon2, tPolygon, sPolygon, key=lambda inptPolygon: (
            unCoveredPolygon.intersection(inptPolygon)).area)
    return polygon

def PolygonCover(polygon, d, coverage, iterations=32):
    polygonCoverList = []
    unCoverPolygon = shapely.Polygon(polygon)
    pool = Pool(32)
    while ((unCoverPolygon.area / polygon.area) > (1-coverage)):

        point = SelectPointFromPolygon(unCoverPolygon)
        R0 = MaximallyCoveringConvexSubset((unCoverPolygon, polygon, point, d))
        bestR = R0
        #迭代开始
        num = iterations
        pointList = []
        while num > 0:
            pointList.append(SelectPointFromPolygon(R0))
            num -= 1
        RList =(pool.map(MaximallyCoveringConvexSubset,[(unCoverPolygon, polygon, point, d) for point in pointList]))
        RList.append(R0)
        bestR = max(RList,key=lambda R:(R.intersection(unCoverPolygon)).area)
        bestR = bestR.simplify(0.05,False)

        polygonCoverList.append(bestR)
        unCoverPolygon = unCoverPolygon.difference(bestR)
        if(type(unCoverPolygon) == shapely.GeometryCollection):
            polygonList = []
            for geoms in unCoverPolygon.geoms:
                if type(geoms) == shapely.Polygon:
                    polygonList.append(geoms)
            unCoverPolygon = shapely.GeometryCollection(polygonList)

    return polygonCoverList
