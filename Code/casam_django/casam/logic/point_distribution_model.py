import vtk

# our data source, a PolyDataReader
#reader = vtk.vtkPolyDataReader()
#reader = vtk.vtkUnstructuredGridReader()
#reader.SetFileName("H:/desktop/landmarks.vtk")
#reader.Update() # by calling Update() we read the file

#pointdata = reader.GetOutput().GetPointData()

# filters we want to use
filterGPA = vtk.vtkProcrustesAlignmentFilter()
filterPCA = vtk.vtkPCAAnalysisFilter()


# Create some landmarks, put them in unstructuredgrid
# Start off with some landmarks
vertexPoints = vtk.vtkPoints()
vertexPoints.SetNumberOfPoints(3)
vertexPoints.InsertPoint(0, 0, 0, 0)
vertexPoints.InsertPoint(1, 3, 1, 0)
vertexPoints.InsertPoint(2, 2, 2, 0)

# Create vertices from them
aVertexa = vtk.vtkVertex()
aVertexa.GetPointIds().SetId(0, 0)
aVertexb = vtk.vtkVertex()
aVertexb.GetPointIds().SetId(0, 1)
aVertexc = vtk.vtkVertex()
aVertexc.GetPointIds().SetId(0, 2)

#Create an unstructured grid with the landmarks added
aVertexGrid = vtk.vtkUnstructuredGrid()
aVertexGrid.Allocate(3, 3)
aVertexGrid.InsertNextCell(aVertexa.GetCellType(), aVertexa.GetPointIds())
aVertexGrid.InsertNextCell(aVertexb.GetCellType(), aVertexb.GetPointIds())
aVertexGrid.InsertNextCell(aVertexc.GetCellType(), aVertexc.GetPointIds())
aVertexGrid.SetPoints(vertexPoints)

#Create a mapper for our data
aVertexMapper = vtk.vtkDataSetMapper()
aVertexMapper.SetInput(aVertexGrid)

#Create the actor
aVertexActor = vtk.vtkActor()
aVertexActor.SetMapper(aVertexMapper)
aVertexActor.GetProperty().SetDiffuseColor(1, 0.5, 1)


#Now for set number 2
# Start off with some landmarks
vertexPoints2 = vtk.vtkPoints()
vertexPoints2.SetNumberOfPoints(3)
vertexPoints2.InsertPoint(0, 0.7, 0, 0)
vertexPoints2.InsertPoint(1, 3.5, 1, 0)
vertexPoints2.InsertPoint(2, 2.3, 2, 0)

# Create vertices from them
aVertexa2 = vtk.vtkVertex()
aVertexa2.GetPointIds().SetId(0, 0)
aVertexb2 = vtk.vtkVertex()
aVertexb2.GetPointIds().SetId(0, 1)
aVertexc2 = vtk.vtkVertex()
aVertexc2.GetPointIds().SetId(0, 2)

#Create an unstructured grid with the landmarks added
aVertexGrid2 = vtk.vtkUnstructuredGrid()
aVertexGrid2.Allocate(3, 3)
aVertexGrid2.InsertNextCell(aVertexa2.GetCellType(), aVertexa2.GetPointIds())
aVertexGrid2.InsertNextCell(aVertexb2.GetCellType(), aVertexb2.GetPointIds())
aVertexGrid2.InsertNextCell(aVertexc2.GetCellType(), aVertexc2.GetPointIds())
aVertexGrid2.SetPoints(vertexPoints2)

#Create a mapper for our data
aVertexMapper2 = vtk.vtkDataSetMapper()
aVertexMapper2.SetInput(aVertexGrid2)

#Create the actor
aVertexActor2 = vtk.vtkActor()
aVertexActor2.SetMapper(aVertexMapper2)
aVertexActor2.GetProperty().SetDiffuseColor(0.5, 1, 1)


#Perform some Procrustes
filterGPA.GetLandmarkTransform().SetModeToRigidBody()
filterGPA.SetNumberOfInputs(2)
filterGPA.SetInput(0,aVertexGrid)
filterGPA.SetInput(1,aVertexGrid2)
print "Performing Generalized Procrustes Analysis..."
filterGPA.Update()
print "Done!"
GPAGrid = filterGPA.GetOutput(0)
GPAGrid2 = filterGPA.GetOutput(1)




#Create a mapper for our data
aVertexMapperGPA = vtk.vtkDataSetMapper()
aVertexMapperGPA.SetInput(GPAGrid)
#Create the actor
aVertexActorGPA = vtk.vtkActor()
aVertexActorGPA.SetMapper(aVertexMapperGPA)
aVertexActorGPA.GetProperty().SetDiffuseColor(1, 0, 0)

#Create a mapper for our data
aVertexMapperGPA2 = vtk.vtkDataSetMapper()
aVertexMapperGPA2.SetInput(GPAGrid2)
#Create the actor
aVertexActorGPA2 = vtk.vtkActor()
aVertexActorGPA2.SetMapper(aVertexMapperGPA2)
aVertexActorGPA2.GetProperty().SetDiffuseColor(0, 1, 0)


#polyDataSet = vtk.vtkPolyData()

#vertexPointsa = vtk.vtkPoints()
#vertexPointsa.SetNumberOfPoints(1)
#vertexPointsa.InsertPoint(0, 0, 0, 0)

#vertexPointsb = vtk.vtkPoints()
#vertexPointsb.SetNumberOfPoints(1)
#vertexPointsb.InsertPoint(0, 3, 1, 0)

#vertexPointsc = vtk.vtkPoints()
#vertexPointsc.SetNumberOfPoints(1)
#vertexPointsc.InsertPoint(0, 2, 2, 0)

#aVertexa = vtk.vtkVertex()
#aVertexa.GetPointIds().SetId(0, 0)
#aVertexb = vtk.vtkVertex()
#aVertexb.GetPointIds().SetId(0, 1)
#aVertexc = vtk.vtkVertex()
#aVertexc.GetPointIds().SetId(0, 2)


#verts = vtk.vtkCellArray()
#verts.InsertNextCell(aVertexa)
#verts.InsertNextCell(aVertexb)
#verts.InsertNextCell(aVertexc)
#polyDataSet.SetVerts(verts)

#polyDataSet.Allocate(3, 3)
#polyDataSet.InsertNextCell(aVertexa.GetCellType(), aVertexa.GetPointIds())
#polyDataSet.InsertNextCell(aVertexb.GetCellType(), aVertexb.GetPointIds())
#polyDataSet.InsertNextCell(aVertexc.GetCellType(), aVertexc.GetPointIds())

#VertexMapper = vtk.vtkPolyDataMapper()
#VertexMapper.SetInput(polyDataSet)

#aVertexActor = vtk.vtkActor()
#aVertexActor.SetMapper(aVertexMapper)
#aVertexActor.AddPosition(0, 0, 0)
#aVertexActor.GetProperty().SetDiffuseColor(1, 1, 1)


#array = reader.GetOutput().GetCellLocationsArray()
#for i in range(15):
#  tuple = reader.GetOutput().GetCell(i).GetBounds()
#  print "Coordinates: ", tuple[0], tuple[2]
#  print reader.GetOutput().GetCell(i).GetPointIds()


# the mapper that will use the lookup table 
#mapper = vtk.vtkPolyDataMapper()
#mapper = vtk.vtkDataSetMapper()
#mapper.SetInput(reader.GetOutput()) # connection
# important! tell which data you want to use
# here we use the point data
#mapper.SetScalarModeToUsePointData() 
#mapper.SetScalarRange(0,4)

# the actor
#myActor = vtk.vtkActor()
#myActor.SetMapper( mapper )

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
#ren.AddActor( myActor )
ren.AddActor( aVertexActor )
ren.AddActor( aVertexActor2 )
ren.AddActor( aVertexActorGPA )
ren.AddActor( aVertexActorGPA2 )

# render
renWin.Render()

# initialize and start the interactor
iren.Initialize()
iren.Start()
