CW = 0
CCW = 1

class WShape(object):
    def __init__(self):
        self.index = 0
        self.vertex_ring = None
        self.edge_ring = None
        self.face_ring = None
        self.next = None
        self.previous = None

    def set_wings(self, e1, e2):
        """
        Takes 2 edges with a common vertex and determines their wing
        information.
        """
        if e1.avertex == e2.avertex:
            if e1.bface == e2.bface:
                e1.bCWedge = e2
                e2.aCCWedge = e1
            elif e1.aface == e2.bface:
                e1.aCCWedge = e2
                e2.bCWedge = e1

        elif e1.avertex == e2.bvertex:
            if e1.bface == e2.bface:
                e1.bCWedge = e2
                e2.bCCWedge = e1
            elif e1.aface == e2.bface:
                e1.aCCWedge = e2
                e2.aCWedge = e1

        elif e1.bvertex == e2.avertex:
            if e1.aface == e2.aface:
                e1.aCWedge = e2
                e2.aCCWedge = e1
            elif e1.bface == e2.bface:
                e1.bCCWedge = e2
                e2.bCWedge = e1

        elif e1.bvertex == e2.bvertex:
            if e1.aface == e2.bface:
                e1.aCWedge = e2
                e2.bCCWedge = e1
            elif e1.bface == e2.aface:
                e1.bCCWedge = e2
                e2.aCWedge = e1

    def face_across_edge(edge, face):
        if edge.aface == face:
            return edge.bface
        elif edge.bface == face:
            return edge.aface

    def next_face_around_vertex(v, face, direction):
        """
        Takes a vertex, a face, and a direction and returns the next face
        around that vertex in the given direction.
        """


class WFace(object):
    def __init__(self):
        self.index = 0
        self.edge_ring = None
        self.next = None
        self.previous = None


class WEdge(object):
    def __init__(self):
        self.edge_data = None
        self.next = None
        self.previous = None


class WVertex(object):
    def __init__(self):
        self.index = 0
        self.point = 0, 0, 0
        self.edge_ring = None
        self.next = None
        self.previous = None


class WEdgeData(object):
    def __init__(self):
        self. = index
        self.aCWedge = None
        self.bCWedge = None
        self.aCCWedge = None
        self.bCCWedge = None
        self.avertex = None
        self.bvertex = None
        self.aface = None
        self.bface = None
        self.owner = None
        
