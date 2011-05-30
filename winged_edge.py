class Edge:
    def __init__(self, name):
        self.name = name
        self.vstart = None
        self.vend = None

        self.fleft = None
        self.fright = None

        self.ltpred = None
        self.ltsucc = None

        self.rtpred = None
        self.rtsucc = None

class Vertex:
    def __init__(self, name):
        self.name = name
        self.incident_edge = None

class Face:
    def __init__(self, name):
        self.name = name
        self.incident_edge = None

class WingedEdge(object):
    def __init__(self, points):
        self.points = points
        self.faces = {}
        self.vertex = {}
        self.edges = {}

        self.edge_table = {}
        self.vertex_table = {}
        self.face_table = {}
    
    def add_face(self, name, p0, p1, p2):
        self.faces[name] = Face(name)
        self.face_table[name] = Face(name)

        if self.vertex_table[p0]:
            e = self.vertex_table[p0].incident_edge
            if e.vend == p1:
                self.face_table[name].incident_edge = e.name
            else:
                e_id = len(self.edge_table)
                edge = Edge(e_id)

                edge.vstart = p0
                edge.vend = p1

                edge.fleft = name

                self.vertex_table[p0].incident_edge = e_id
                self.face_table[name].incident_edge = e_id
                
        
        id_edge = len(self.vextex)
        self.vertex[id_edge] = p0, p1
        self.vertex[id_edge + 1] = p1, p2
        self.vertex[id_edge + 2] = p2, p0

