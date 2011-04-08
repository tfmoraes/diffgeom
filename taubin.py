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
    cell_ids = vtk.vtkIdList()
    p = mesh.GetPoint(pid)
    mesh.GetPointCells(pid, cell_ids)
    for i in xrange(cell_ids.GetNumberOfIds()):
        point_ids = vtk.vtkIdList()
        mesh.GetCellPoints(cell_ids.GetId(i), point_ids)
        n += 1
        if point_ids.GetId(0) != pid:
            np = mesh.GetPoint(point_ids.GetId(0))
        else:
            np = mesh.GetPoint(point_ids.GetId(1))

        tx = tx + (np[0] - p[0])
        ty = ty + (np[1] - p[1])
        tz = tz + (np[2] - p[2])

    tx, ty, tz =  tx / n, ty / n, tz / n
    return tx, ty, tz

        

def taubin_smooth(poly, l, m, steps):
    trianglefilter = vtk.vtkTriangleFilter()
    trianglefilter.SetInput(poly)
    trianglefilter.Update()

    edgesfilter = vtk.vtkExtractEdges()
    edgesfilter.SetInput(trianglefilter.GetOutput())
    edgesfilter.Update()

    edges = edgesfilter.GetOutput()

    new_poly = vtk.vtkPolyData()
    new_poly.DeepCopy(trianglefilter.GetOutput())

    points = new_poly.GetPoints()
    for s in xrange(steps):
        D = {}
        for i in xrange(edges.GetNumberOfPoints()):
            D[i] = calculate_d(edges, i)
        for i in xrange(poly.GetNumberOfPoints()):
            x, y, z = points.GetPoint(i)
            x = x + l*D[i][0]
            y = y + l*D[i][1]
            z = z + l*D[i][2]
            points.SetPoint(i, x, y, z)

        D = {}
        for i in xrange(edges.GetNumberOfPoints()):
            D[i] = calculate_d(edges, i)
        for i in xrange(poly.GetNumberOfPoints()):
            x, y, z = points.GetPoint(i)
            x = x + m*D[i][0]
            y = y + m*D[i][1]
            z = z + m*D[i][2]
            points.SetPoint(i, x, y, z)

    new_poly.SetPoints(points)
    return new_poly
    

def main():
    poly = load_file(sys.argv[1])
    steps = int(sys.argv[3])
    
    new_poly = taubin_smooth(poly, 0.5, -0.53, steps)

    w = vtk.vtkSTLWriter()
    w.SetFileName(sys.argv[2])
    w.SetInput(new_poly)
    w.SetFileTypeToBinary()
    w.Write()

if __name__ == '__main__':
    main()
