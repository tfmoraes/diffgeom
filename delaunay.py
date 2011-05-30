import numpy as np
import math

import winged_edge

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

class Node(object):
    def __init__(self, triangle):
        self.triangle = triangle
        self.children = None

class Tree(object):
    def __init__(self, triangle_root):
        self.triangles = [triangle_root]
        self.root = Node(triangle_root)

    def add(self, point):
        if self.root.children:
            pass
        else:
            t0 = self.triangles[0]
            t1 = Triangle(point, t0.p0, t0.p1)
            t2 = Triangle(point, t0.p1, t0.p2)
            t3 = Triangle(point, t0.p2, t0.p0)

            t0.children = [t1, t2, t3]
        
        


class DelaunayTriangulation(object):
    def __init__(self, points):
        self.points = dict(zip(xrange(len(points)), points))
        self.winged_edge = winged_edge.WingedEdge(self.points)

    def make_delaunay_triangulation(self):
        points = self.points.values()
        points.sort(key=lambda x: [x[1], x[0]])

        p0 = points[-1]
        p_1 = points[0] - 1, 1000
        p_2 = points[-1] + 1, -1000

        t0 = Triangle(p0, p_1, p_2)
        self.tree = Tree(t0)

        vertices = self.points[:-1]
        np.random.shuffle(vertices)

        for r in vertices:
            self.tree.add(r)


def main():
    import random
    points = [(random.random(), random.random()) for i in xrange(10)]

    t = DelaunayTriangulation(points)

if __name__ == '__main__':
    main()
