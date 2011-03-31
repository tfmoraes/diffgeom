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

def main():
    poly = load_file('monkey.ply')
    poly.BuildLinks(0)
    np = poly.GetNumberOfPoints()

    Ls = numpy.zeros((np, np))
    X, Y, Z = numpy_support.vtk_to_numpy(poly.GetPoints().GetData()).transpose()

    for i in xrange(np):
        for j in xrange(np):
            if i != j :
                if poly.IsEdge(i, j):
                    Ls[i, j] = -1
                    Ls[i, i] += 1

    Ls = numpy.matrix(Ls)
    Dx = X * Ls
    Dy = Y * Ls
    Dz = Z * Ls
    
    Dxg = gaussian_filter1d(Dx, 1)
    Dyg = gaussian_filter1d(Dy, 1)
    Dzg = gaussian_filter1d(Dz, 1)

    #Lsn = numpy.linalg.inv(Ls)

    #Xn = Lsn * Dxg
    #Yn = Lsn * Dyg
    #Zn = Lsn * Dzg

    X[:] = numpy.linalg.lstsq(Ls, Dxg.transpose())
    Y[:] = Dyg[0, :]
    Z[:] = Dzg[0, :]

    print X.shape
    
    V = numpy.zeros((np, 3))
    V[:,0] = X
    V[:,1] = Y
    V[:,2] = Z

    poly.GetPoints().SetData(numpy_support.numpy_to_vtk(V))
    poly.BuildLinks(0)
    poly.BuildCells()

    w = vtk.vtkSTLWriter()
    w.SetFileName('/tmp/teste.stl')
    w.SetInput(poly)
    w.Write()

if __name__ == '__main__':
    main()
