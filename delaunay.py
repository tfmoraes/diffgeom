import numpy as np
import math

class Triangle(object):
    def __init__(self, p0, p1, p2):
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2

    def is_inside(self, point):
        m = np.matrix([[self.p0[0], self.p0[1], self.p0[0]**2 + self.p0[1]**2, 1],
                       [self.p1[0], self.p1[1], self.p1[0]**2 + self.p1[1]**2, 1],
                       [self.p2[0], self.p2[1], self.p2[0]**2 + self.p2[1]**2, 1],
                       [point[0], point[1], point[0]**2 + point[1]**2,1]])
        return np.linalg.det(m) > 0

class Tree(object):
    def __init__(self):
        pass

    def add(self, point):
        pass


class DelaunayTriangulation(object):
    def __init__(self, points):
        self.points = points

    def make_delaunay_triangulation(self):
        self.points.sort(key=lambda x: [x[1], x[0]])
        p0 = self.points[-1]
        p_1 = self.points[0] - 1, 1000
        p_2 = self.points[-1] + 1, -1000

        vertices = self.points[:-1]
        np.random.shuffle(vertices)

        for r in vertices:
            pass

