import sys

import numpy as np
import vtk

from vtk.util import numpy_support

def load_file(filename):
    if filename.endswith('.ply'):
        reader = vtk.vtkPLYReader()
    else:
        reader = vtk.vtkSTLReader()
    reader.SetFileName(filename)
    reader.Update()
    return reader.GetOutput()

def calculate_d(mesh, poly, pid):
    t = 0
    n = 0.0
    cell_ids = vtk.vtkIdList()
    p0 = np.array(poly.GetPoint(pid))
    mesh.GetPointCells(pid, cell_ids)
    for i in xrange(cell_ids.GetNumberOfIds()):
        point_ids = vtk.vtkIdList()
        mesh.GetCellPoints(cell_ids.GetId(i), point_ids)
        n += 1
        if point_ids.GetId(0) != pid:
            p1 = np.array(poly.GetPoint(point_ids.GetId(0)))
        else:
            p1 = np.array(poly.GetPoint(point_ids.GetId(1)))

        t = t + (p1 - p0)

    return t / n

def taubin_smooth(poly, l, m, steps):
    edgesfilter = vtk.vtkExtractEdges()
    edgesfilter.SetInput(poly)
    edgesfilter.Update()

    edges = edgesfilter.GetOutput()

    new_poly = vtk.vtkPolyData()
    new_poly.DeepCopy(poly)

    print edges.GetNumberOfPoints()
    print poly.GetNumberOfPoints()

    points = new_poly.GetPoints()
    for s in xrange(steps):
        D = {}
        for i in xrange(edges.GetNumberOfPoints()):
            D[i] = calculate_d(edges, new_poly, i)
        for i in xrange(poly.GetNumberOfPoints()):
            p = np.array(points.GetPoint(i))
            pl = p + l*D[i]
            nx, ny, nz = pl
            points.SetPoint(i, nx, ny, nz)

        D = {}
        for i in xrange(edges.GetNumberOfPoints()):
            D[i] = calculate_d(edges, new_poly, i)
        for i in xrange(poly.GetNumberOfPoints()):
            p = np.array(points.GetPoint(i))
            pl = p + m*D[i]
            nx, ny, nz = pl
            points.SetPoint(i, nx, ny, nz)

        #D = {}
        #for i in xrange(edges.GetNumberOfPoints()):
            #D[i] = calculate_d(edges, i)
        #for i in xrange(poly.GetNumberOfPoints()):
            #x, y, z = points.GetPoint(i)
            #nx = x + m*D[i][0]
            #ny = y + m*D[i][1]
            #nz = z + m*D[i][2]
            #points.SetPoint(i, nx, ny, nz)

    #new_poly.SetPoints(points)
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
