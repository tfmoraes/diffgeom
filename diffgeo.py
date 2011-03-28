import vtk
import sys
import numpy

def load_file(filename):
    reader = vtk.vtkPLYReader()
    reader.SetFileName(filename)
    reader.Update()
    return reader.GetOutput()

def main():
    poly = load_file('monkey.ply')
    poly.BuildLinks(0)
    np = poly.GetNumberOfPoints()

    for i in xrange(np):
        for j in xrange(np):
            if i != j :
                poly.IsEdge(i, j)
    


if __name__ == '__main__':
    main()
