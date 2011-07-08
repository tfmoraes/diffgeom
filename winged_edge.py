class WShape(object):
    def __init__(self):
        self.index = 0
        self.vertex_ring = None
        self.edge_ring = None
        self.face_ring = None
        self.next = None
        self.previous = None


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
        

