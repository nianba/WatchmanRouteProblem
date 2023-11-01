import cv2
import numpy as np
import shapely
from ..Global import *
def DrawPolygon( points, color, image, zoomRate = 1):

    points = np.array(points)
    points *= zoomRate
    points = np.round(points).astype(np.int32)

    if type(points) is np.ndarray and points.ndim == 2:
        image = cv2.fillPoly(image, [points], color,8)
    else:
        image = cv2.fillPoly(image, points, color,8)

    return image


def DrawPoints(image, x, y, color=(153, 92, 0),size = -1,zoomRate = 1):
    x = np.round(x*zoomRate).astype(np.int32)
    y = np.round(y*zoomRate).astype(np.int32)
    cv2.circle(image, (x, y), 1, color, size)
    return image

def DrawSinglePoint(image, x, y, color=30,size = -1,zoomRate=1):
    x = np.round(x*zoomRate).astype(np.int32)
    y = np.round(y*zoomRate).astype(np.int32)
    image[y-1:y+2,x-1:x+2] = color
    return image

def DrawGridNum(image, x, y, num,zoomRate = 1):

    x = np.round(x*zoomRate).astype(np.int32)
    y = np.round(y*zoomRate).astype(np.int32)
    s_num = str(num)
    cv2.putText(image, s_num, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 0), 1)
def DrawLine(image, pt1, pt2,color = (0, 25, 255),zoomRate = 1):


    # x1 = int(pt1[0])
    # y1 = int(pt1[1])
    # x2 = int(pt2[0])
    # y2 = int(pt2[1])
    x1 = np.round(pt1[0] * zoomRate).astype(np.int32)
    y1 = np.round(pt1[1] * zoomRate).astype(np.int32)
    x2 = np.round(pt2[0] * zoomRate).astype(np.int32)
    y2 = np.round(pt2[1] * zoomRate).astype(np.int32)
    cv2.line(image, (x1, y1), (x2, y2), color, 1)

def DrawPath(image, path):
    i = 0
    while i < len(path)-1:
        DrawLine(image, path[i], path[i+1])
        i += 1
def DrawMultiline(image, multiLine,color = (0, 25, 255),zoomRate = 1):
    
    def drawSingleline(image,line,color = (0, 25, 255),zoomRate = 1):
        pointList = list(line.coords)
        length = len(pointList)
        for i in range(length-1):
            DrawLine(image,pointList[i],pointList[i+1],color,zoomRate=zoomRate)

    if(type(multiLine) == shapely.Point):
        return
    elif(type(multiLine) == shapely.LineString):
        drawSingleline(image,multiLine,color,zoomRate=zoomRate)
    elif(type(multiLine) == shapely.Polygon):
        DrawPolygon(list(multiLine.exterior.coords),color,image,zoomRate=zoomRate)
    elif(type(multiLine) == shapely.MultiLineString):
        for line in list(multiLine.geoms):
            drawSingleline(image,line,color,zoomRate=zoomRate)
    elif(type(multiLine) == shapely.GeometryCollection):
        for geometry in multiLine.geoms:
            DrawMultiline(image,geometry,color=color,zoomRate=zoomRate)
    elif(type(multiLine) == shapely.MultiPolygon):
        for geometry in multiLine.geoms:
            DrawMultiline(image,geometry,color=color,zoomRate=zoomRate)
    else:
        print(type(multiLine))
        print("unknown type")