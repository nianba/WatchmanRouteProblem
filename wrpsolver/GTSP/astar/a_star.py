
import math
from . import AStar


class AStarSolver(AStar):

    """sample use of the astar algorithm. In this exemple we work on a maze made of ascii characters,
    and a 'node' is just a (x,y) tuple that represents a reachable position"""

    def __init__(self,grid):
        self.grid = grid
        self.step = 3
        self.y_len = self.grid.shape[0]
        self.x_len = self.grid.shape[1]
    def isReachable(self, point):
        grid = self.grid
        (x,y) = point
        if(x<0 or y <0 or x>=self.x_len or y>=self.y_len):
            return False
        return grid[y][x] != 0 #这里没写错


    def heuristic_cost_estimate(self, n1, n2):
        """computes the 'direct' distance between two (x,y) tuples"""
        (x1, y1) = n1
        (x2, y2) = n2
        return math.hypot(x2 - x1, y2 - y1)

    def distance_between(self, n1, n2):
        """this method always returns 1, as two 'neighbors' are always adajcent"""
        # (x1, y1) = n1
        # (x2, y2) = n2
        # return math.hypot(x2 - x1, y2 - y1)
        return 1

    def neighbors(self, node):
        """ for a given coordinate in the maze, returns up to 4 adjacent(north,east,south,west)
            nodes that can be reached (=any adjacent coordinate that is not a wall)
        """

        x, y = node
        step = self.step
        miniStep = 1
        neighborList = [
                        (x+step, y), (x-step, y),
                        (x, y+step), (x, y-step),
                        # (x-step,y-step),(x+step,y+step),
                        # (x+step,y-step),(x-step,y+step),

                        # (x+miniStep, y), (x-miniStep, y),
                        # (x, y+miniStep), (x, y-miniStep),
                        # (x-miniStep,y-miniStep),(x+miniStep,y+miniStep),
                        # (x+miniStep,y-miniStep),(x-miniStep,y+miniStep),
                        ]
        nbs = [neighbor for neighbor in neighborList if self.isReachable(neighbor)]
        return nbs

    def is_goal_reached(self, current, goal) -> bool:
        return current == goal

def findPath(start, goal, grid):

    # let's solve it
    aStarSolver = AStarSolver(grid)
    result = aStarSolver.astar(start, goal)
    foundPath = list(result)
    distance = len(foundPath) * aStarSolver.step

    return foundPath, distance
