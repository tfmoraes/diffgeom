import sys

import numpy
import vtk

from vtk.util import numpy_support
from scipy.ndimage import gaussian_filter1d

def load_file(filename):
    reader = vtk.vtkPLYReader()
    reader.SetFileName(filename)
    reader.Update()
    return reader.GetOutput()

def taubin_smooth(poly, l, m):
    np = poly.GetNumberOfPoints()
    X, Y, Z = numpy_support.vtk_to_numpy(poly.GetPoints().GetData()).transpose()
    W = numpy.zeros((np, np))
    I = numpy.identity(np)

    for i in xrange(np):
        for j in xrange(np):
            if i != j :
                if poly.IsEdge(i, j):
                    W[i, j] += 1
    W = 1.0 / W
    W[W == numpy.inf] = 0
    K = numpy.matrix(I - W)
    for i in xrange(10):
        
        if i%2:
            t = I - m*K
        else:
            t = I - l*K

        print t.shape, X.shape

        dx = X*t
        dy = Y*t
        dz = Z*t

        X[:] = dx
        Y[:] = dy
        Z[:] = dz

    return X, Y, Z, np

    

def main():
    poly = load_file('monkey.ply')
    poly.BuildLinks(0)

    X, Y, Z, np =taubin_smooth(poly, 0.5, -0.53)

    V = numpy.zeros((np, 3))
    V[:,0] = X
    V[:,1] = Y
    V[:,2] = Z


    new_polydata = vtk.vtkPolyData()
    new_polydata.DeepCopy(poly)
    new_polydata.GetPoints().SetData(numpy_support.numpy_to_vtk(V))
    new_polydata.Update()
    #new_polydata.BuildLinks(0)
    #new_polydata.BuildCells()

    w = vtk.vtkSTLWriter()
    w.SetFileName('/tmp/teste.stl')
    w.SetInput(new_polydata)
    w.Write()

if __name__ == '__main__':
    main()
