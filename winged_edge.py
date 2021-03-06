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
        for e in face.edge_ring:
            if direction == CW:
                if face == e.aface:
                    if e.avertex == v:
                        return face_across_edge(e.edge_data.aCCWedge, face)
                    elif e.bvertex == v:
                        return face_across_edge(e, face)
                elif face == e.bface:
                    if e.avertex == v:
                        return face_across_edge(e, face)
                    elif e.bvertex == v:
                        return face_across_edge(e.edge_data.bCCWedge, face)
            elif direction == CCW:
                if face == e.aface:
                    if e.avertex == v:
                        return face_across_edge(e, face)
                    elif e.bvertex == v:
                        return face_across_edge(e.edge_data.aCWedge, face)
                elif face == e.bface:
                    if e.avertex == v:
                        return face_across_edge(e.edge_data.bCWedge, face)
                    elif e.bvertex == v:
                        return face_across_edge(e, face)

    def split_edge(self, edge):
        v0 = edge.edge_data.avertex.point
        v1 = edge.edge_data.bvertex.point
        v2 = (v0 + v1) / 2.0
        
        en = WEdge()
        vn = WVertex() 
        vn.point = v2

        self.edge_ring.append(en)
        self.vertex_ring.append(vn)

        edge.edge_data.aface.edge_ring.append(en)
        edge.edge_data.bface.edge_ring.append(en)

        en.edge_data.avertex = vn
        en.edge_data.bvertex = edge.edge_data.bvertex
        edge.edge_data.bvertex = vn

        en.edge_data.aCWedge = edge.edge_data.aCWedge
        en.edge_data.bCCWedge = edge.edge_data.bCCWedge

        en.edge_data.bCWedge = edge
        en.edge_data.aCCWedge = edge

        edge.edge_data.bCCWedge = en
        edge.edge_data.aCCWedge = en

    def remove_edge(self, edge):
        edge.edge_data.avertex = None
        edge.edge_data.bvertex = None

        # STEP 3: Repoint all edges pointing to face b to point to face a
        for e in edge.edge_data.bface.edge_ring:
            if e.edge_data.aface == edge.edge_data.bface:
                e.edge_data.aface = edge_data.aface
            else:
                e.edge_data.bface = edge_data.aface

        # TODO: STEP 4, 5 and 6
        del edge.edge_data.bface
        del edge


    

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
        self.index = 0
        self.aCWedge = None
        self.bCWedge = None
        self.aCCWedge = None
        self.bCCWedge = None
        self.avertex = None
        self.bvertex = None
        self.aface = None
        self.bface = None
        self.owner = None
        
