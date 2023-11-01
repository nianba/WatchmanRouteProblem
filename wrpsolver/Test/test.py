#!/usr/bin/python3.8
# -*- coding:utf-8 -*-
import cv2
import shapely
import math
import os
from . import vis_maps
from ..WRP_solver import WatchmanRouteProblemSolver
from .draw_pictures import *

def RunTest(seed = 1):
    iterationNum = 64
    d = 60
    coverageRate = 0.98

    # 随机生成多边形
    path = os.path.dirname(os.path.realpath(__file__))+'/../../test'
    os.makedirs(path,exist_ok=True)
    pointList,_,_ = vis_maps.GetPolygon(seed)
    polygon = shapely.Polygon(pointList).simplify(0.05,True).buffer(-0.7,join_style=2)
    if(type(polygon) != shapely.Polygon):
        print(type(polygon))
        return
    print("polygon area: ", polygon.area)
    minx, miny, maxx, maxy = polygon.bounds
    maxx = math.ceil(maxx/10)*10
    maxy = math.ceil(maxy/10)*10
    image = np.zeros((int(maxy), int(maxx), 3), dtype=np.uint8)
    DrawPolygon( list(polygon.exterior.coords), (255, 255, 255), image, zoomRate=1)
    cv2.imwrite('test/test.png',image)
    image1 = cv2.resize(image,(100,100),interpolation = cv2.INTER_NEAREST)
    cv2.imwrite('test/test0.png',image1)

    polygonCoverList, sampleList,order, length, path, _ = WatchmanRouteProblemSolver(
        polygon, coverageRate, d, iterationNum)
    print("The number of convex polygonlen is " + str(len(polygonCoverList)))
    print("path length ", length)
    length = 0
    for sample in sampleList:
        length += len(sample)
    print("samples " , length)

    # 绘制生成的多边形
    DrawPolygon( list(polygon.exterior.coords), (255, 255, 255), image, zoomRate=1)
    cv2.imwrite('test/test1.png',image)
    colorList = []
    for n in range(192,-1,-64):
        for m in range(256,-1,-64):
            for o in range(256,-1,-64):
                colorList.append((o,m,n))
    cnt = 0
    for p in polygonCoverList:
        image = image.copy()
        p = p.simplify(0.05, preserve_topology=False)
        DrawPolygon( list(p.exterior.coords), colorList[cnt], image, zoomRate=1)
        cv2.imwrite('test/test2_'+ str(cnt) +'.png',image)
        cnt += 1

    # 绘制sample 和 访问顺序
    for sample in sampleList:
        for point in sample:
            DrawPoints(image, point[0], point[1],zoomRate=(1))
            pass
    cv2.imwrite('test/test3.png',image)

    for i in range(len(path)):
        pass
        DrawPath(image, path[i])
    cv2.imwrite('test/test4.png',image)

    for i in range(len(order)):
        DrawPoints(image, order[i][0], order[i][1],(0,255,0),1)
    cv2.imwrite('test/test5.png',image)

