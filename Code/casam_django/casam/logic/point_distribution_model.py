import vtk

# our data source, a PolyDataReader
#reader = vtk.vtkPolyDataReader()
reader = vtk.vtkUnstructuredGridReader()
reader.SetFileName("H:/desktop/landmarks.vtk")
reader.Update() # by calling Update() we read the file

# find the range of the point scalars
pointdata = reader.GetOutput().GetPointData()

# show how to print a string in python
print "O Hi!" 
print "Points: %s" %(pointdata)


array = reader.GetOutput().GetCellLocationsArray()
for i in range(15):
  print reader.GetOutput().GetCell(i)
  print reader.GetOutput().GetCell(i).GetNumberOfPoints()


# the mapper that will use the lookup table 
#mapper = vtk.vtkPolyDataMapper()
mapper = vtk.vtkDataSetMapper()
mapper.SetInput(reader.GetOutput()) # connection
# important! tell which data you want to use
# here we use the point data
mapper.SetScalarModeToUsePointData() 
mapper.SetScalarRange(0,14)

# the actor
myActor = vtk.vtkActor()
myActor.SetMapper( mapper )

# renderer and render window 
ren = vtk.vtkRenderer()
ren.SetBackground(0, 0, 0)
renWin = vtk.vtkRenderWindow()
renWin.SetSize(300, 300)
renWin.AddRenderer( ren )

# render window interactor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow( renWin )

# add the actors to the renderer
ren.AddActor( myActor )

# render
renWin.Render()

# initialize and start the interactor
iren.Initialize()
iren.Start()