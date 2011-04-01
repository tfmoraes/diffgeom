import sys

import numpy
import vtk

from vtk.util import numpy_support
from scipy.ndimage import gaussian_filter1d

def load_file(filename):
    if filename.endswith('.ply'):
        reader = vtk.vtkPLYReader()
    else:
        reader = vtk.vtkSTLReader()
    reader.SetFileName(filename)
    reader.Update()
    return reader.GetOutput()

def calculate_d(mesh, pid):
    tx, ty, tz = 0, 0, 0
    n = 0.0
    cids = vtk.vtkIdList()
    p = mesh.GetPoint(pid)
    mesh.GetPointCells(pid, cids)
    for i in xrange(cids.GetNumberOfIds()):
        point_ids = vtk.vtkIdList()
        mesh.GetCellPoints(cids.GetId(i), point_ids)
        n += 1
        if point_ids.GetId(0) != pid:
            np = mesh.GetPoint(point_ids.GetId(0))
        else:
            np = mesh.GetPoint(point_ids.GetId(1))

        tx = tx + (np[0] - p[0])
        ty = ty + (np[1] - p[1])
        tz = tz + (np[2] - p[2])

    return tx / n, ty / n, tz / n

        

def taubin_smooth(poly, l, m):
    trianglefilter = vtk.vtkTriangleFilter()
    trianglefilter.SetInput(poly)
    trianglefilter.Update()

    edgesfilter = vtk.vtkExtractEdges()
    edgesfilter.SetInput(poly)
    edgesfilter.Update()

    edges = edgesfilter.GetOutput()

    D = {}
    for i in xrange(edges.GetNumberOfPoints()):
        D[i] = calculate_d(edges, i)

    points = poly.GetPoints()
    for s in xrange(10):
        for i in xrange(poly.GetNumberOfPoints()):
            x, y, z = points.GetPoint(i)
            if s%2 == 0:
                x = x + l*D[i][0]
                y = y + l*D[i][1]
                z = z + l*D[i][2]
            else:
                x = x + m*D[i][0]
                y = y + m*D[i][1]
                z = z + m*D[i][2]
            points.SetPoint(i, x, y, z)

    poly.SetPoints(points)
    

def main():
    poly = load_file(sys.argv[1])
    taubin_smooth(poly, 0.5, -0.53)

    w = vtk.vtkSTLWriter()
    w.SetFileName(sys.argv[2])
    w.SetInput(poly)
    w.SetFileTypeToBinary()
    w.Write()

if __name__ == '__main__':
    main()
