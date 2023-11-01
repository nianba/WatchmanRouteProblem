import shapely
import operator
import math
def GetRayLine(watcher, vertex):
    xGap = vertex[0] - watcher[0]
    yGap = vertex[1] - watcher[1]
    rate =  (1/(math.hypot(xGap, yGap)))*1e10
    extendPoint1 = (watcher[0] + xGap*rate,watcher[1] + yGap*rate)
    extendPoint2 = (watcher[0] - xGap*rate,watcher[1] - yGap*rate)
    return shapely.LineString([extendPoint1, extendPoint2])


def judgeVisible(polygon, watcher, vertex, shortenRate=0.001):
    if(polygon.covers(shapely.LineString([watcher,vertex]))):
        return True

    return False


def GetIntersectPointList(intersection):
    pointList = []
    if (type(intersection) == shapely.Point):
        pointList.append(intersection)
    elif (type(intersection) == shapely.MultiPoint):
        pointList = list(intersection.geoms)
    elif (type(intersection) == shapely.GeometryCollection):
        for geometry in list(intersection.geoms):
            if (type(geometry) == shapely.Point):
                pointList.append(geometry)
            elif (type(geometry) == shapely.LineString):
                pass
            else:
                print("Unknown geometry type !")
                return None
    return pointList

def GetVisibilityPolygon(polygon, watcher):

    polygon = polygon.simplify(0.05, preserve_topology=False)
    visibilityPolygon = []
    result = []
    if not polygon.covers(watcher):
        print("The point should be within polygon!")
        return visibilityPolygon
    vertexsList = list(polygon.exterior.coords)
    vertexsList.pop()  # 去除重复点
    vertexsList.reverse()  # 让点按照逆时针排序
    for vertex in vertexsList:

        rayLine = GetRayLine((watcher.x, watcher.y), vertex)
        intersections = (polygon.boundary).intersection(rayLine)
        intersectPointList = GetIntersectPointList(intersections)
        intersectPointList.append(shapely.Point(vertex))

        for intersectPoint in intersectPointList:
            if (judgeVisible(polygon, watcher, intersectPoint)):
                visibilityPolygon.append(intersectPoint)
                
    visibilityPolygon = sorted(visibilityPolygon, key=lambda coord: (-135 - math.degrees(math.atan2(*
                                                                              tuple(map(operator.sub, (coord.x,coord.y), (watcher.x, watcher.y)))[::-1]))) % 360, reverse=False)
    bndry = (polygon.boundary.coords)
    lineStrings = [shapely.LineString(bndry[k:k+2])
                   for k in range(len(bndry) - 1)]

    for lineString in lineStrings:
        for point in visibilityPolygon:
            if lineString.covers(point):
                result.append(point)

    return shapely.Polygon(result).simplify(0.5,False)