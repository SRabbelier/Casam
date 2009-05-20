import colorsys
import logging

import vtk


def getColors(colors):
  """Return RGB color-range
  """

  return [colorsys.hsv_to_rgb(x*1.0/colors, 1, 1) for x in range(colors)]


class PointDistributionModel(object):
  """Calculates the Point Distribution Model using an unstructured grid
  """
  
  def __init__(self):
    """
    """

    self.filterGPA = vtk.vtkProcrustesAlignmentFilter()
    self.filterPCA = vtk.vtkPCAAnalysisFilter()

    self.renderer = vtk.vtkRenderer()
    self.renderer.SetBackground(0, 0, 0)
    #self.renderer.ResetCamera(0,600,0,400,0,0)

    self.renderWindow = vtk.vtkRenderWindow()
    self.renderWindow.SetSize(600, 400)
    self.renderWindow.AddRenderer( self.renderer )
  
    # render window interactor
    self.windowInteractor = vtk.vtkRenderWindowInteractor()
    self.windowInteractor.SetRenderWindow(self.renderWindow)

    self.vertexGrids = []
    self.alignedGrids = []
    self.analyzedGrids = []
    self.meanShape = [] 

    self.colors = getColors(10)

  def addPointSet(self, data):
    """Add a set of points to the UnstructuredGrid vertexGrid (the source of our calculations)
    """

    logging.info("adding point set")

    size = len(data)

    # Create some landmarks, put them in UnstructuredGrid
    # Start off with some landmarks
    vertexPoints = vtk.vtkPoints()
    vertexPoints.SetNumberOfPoints(size)

    vertexGrid = vtk.vtkUnstructuredGrid()
    vertexGrid.Allocate(size, size)

    for id, (x, y, z) in enumerate(data):
      vertexPoints.InsertPoint(id, x, y, z)

      # Create vertices from them
      vertex = vtk.vtkVertex()
      vertex.GetPointIds().SetId(0, id)

      #Create an unstructured grid with the landmarks added
      vertexGrid.InsertNextCell(vertex.GetCellType(), vertex.GetPointIds())
  
    vertexGrid.SetPoints(vertexPoints)
    self.vertexGrids.append(vertexGrid)
    
    logging.info("done")
  
  def addActors(self, grids, colorid):
    """Add UnstructuredGrid actors to the renderer.
    """

    logging.info("adding actors")

    for id, grid in enumerate(grids):
      #Create a mapper for our data
      vertexMapper = vtk.vtkDataSetMapper()
      vertexMapper.SetInput(grid)
      
      #Create the actor
      vertexActor = vtk.vtkActor()
      vertexActor.SetMapper(vertexMapper)
      vertexActor.GetProperty().SetDiffuseColor(self.colors[colorid])
      
      # add the actors to the renderer
      self.renderer.AddActor( vertexActor )
    
    logging.info("done")

  def procrustes(self):
    """Performs Generalized Procrustes Analysis on the vertexGrids. Results are stored in alignedGrids.
    """

    logging.info("running procrustes")

    size = len(self.vertexGrids)

    self.filterGPA.SetNumberOfInputs(size)
    self.filterGPA.GetLandmarkTransform().SetModeToRigidBody()

    for id, grid in enumerate(self.vertexGrids):
      self.filterGPA.SetInput(id, grid)
      
    self.filterGPA.Update()

    for id in range(size):
      grid = self.filterGPA.GetOutput(id)
      self.alignedGrids.append(grid)
      
    logging.info("done")
  
  def pca(self):
    """Performs Principle Component Analysis on the alignedGrids. Also calculates the mean shape.
    """

    logging.info("running pca")

    size = len(self.alignedGrids)

    self.filterPCA.SetNumberOfInputs(size)
    
    for id, grid in enumerate(self.alignedGrids):    
      self.filterPCA.SetInput(id, grid)

    self.filterPCA.Update()
        
    #Get the eigenvalues
    evals = self.filterPCA.GetEvals()
    
    #And the eigenvectors
    numEigenVectors = 5
    evecArrays = []
    for vecId in range(min(numEigenVectors, self.filterPCA.GetNumberOfOutputPorts())):
        out = self.filterPCA.GetOutput(vecId)
        evecs = vtk.vtkFloatArray()
        evecs.SetNumberOfComponents(3)
        evecs.SetName("evecs%d" % vecId)
        # Each point is in fact a vector eval * evec
        for pointId in range(out.GetNumberOfPoints()):
            vec = out.GetPoint(pointId)
            evecs.InsertNextTuple3(vec[0], vec[1], vec[2])
        evecArrays.append(evecs)

        eigenvector = evecArrays[vecId]
        print "E-vector ", vecId, "E-value: ", evals.GetValue(vecId), "X: ", eigenvector.GetValue(0), "Y: ", eigenvector.GetValue(1), "Z: ", eigenvector.GetValue(2)
    
    print "To explain 99% of variation, we need: ", self.filterPCA.GetModesRequiredFor(0.99), " eigenvectors"

    #Now let's get mean ^^
    b = vtk.vtkFloatArray()
    b.SetNumberOfComponents(0)
    b.SetNumberOfTuples(0)
    mean = vtk.vtkUnstructuredGrid()
    mean.DeepCopy(self.alignedGrids[0])
    #Get the mean shape:
    self.filterPCA.GetParameterisedShape(b, mean)
    self.meanShape.append(mean)   

    logging.info("done")
    
  def variations(self):
    """Calculate the extremes of the first two modes of variation (plus and minus 3 standard deviations)
    """
    
    b = vtk.vtkFloatArray()
    #to calculate the first mode of variation extremes (-3 standard deviations and + 3)
    b.SetNumberOfComponents(1)
    b.SetNumberOfTuples(1)
    
    tuples = (0,-3.0), (0,3.0) ,(1,-3.0), (1,3.0)
    for tuple in tuples:
      if tuple[0] == 1: #For the 2nd mode of variation, disable the first!
        b.SetNumberOfTuples(2)
        b.SetTuple1(0, 0.0)
      b.SetTuple1(tuple[0], tuple[1]) 
      extreme = vtk.vtkUnstructuredGrid()
      extreme.DeepCopy(self.alignedGrids[0])
      self.filterPCA.GetParameterisedShape(b, extreme)
      self.analyzedGrids.append(extreme)
      
  
  def visualizeMean(self):
    """Visualize the mean shape by creating a sphere for each mean landmark point
    """
    
    #Get the mean shape locations and make some shiny red spheres for each one
    for id in range(self.meanShape[0].GetNumberOfCells()):
      coords = self.meanShape[0].GetCell(id).GetBounds()
      landmarkSphere = vtk.vtkSphereSource()
      landmarkSphere.SetCenter(coords[0], coords[2], 0)
      landmarkSphere.SetRadius(10)
      landmarkMapper = vtk.vtkPolyDataMapper()
      landmarkMapper.SetInputConnection(landmarkSphere.GetOutputPort())
      landmarkActor = vtk.vtkActor()
      landmarkActor.SetMapper(landmarkMapper)
      landmarkActor.GetProperty().SetDiffuseColor(1,0,1)
      landmarkActor.GetProperty().SetOpacity(0.5)
      self.renderer.AddActor(landmarkActor)
    
  def render(self):
    """Set up rendering and save the results to a PNG-file
    """

    logging.info("rendering")
    
    self.renderWindow.Render()    
 
    # initialize and start the interactor
    self.windowInteractor.Initialize()
    self.windowInteractor.Start()
    
    #Render the image into a png
    renderLarge = vtk.vtkRenderLargeImage()
    renderLarge.SetMagnification(1)
    renderLarge.SetInput(self.renderer)

    writer = vtk.vtkPNGWriter()
    writer.SetInputConnection(renderLarge.GetOutputPort())
    writer.SetFileName("H:/Desktop/Renderedimage.png")
    writer.Write()
    
    logging.info("done")


def main():
  logging.basicConfig(level=logging.DEBUG)
  pdm = PointDistributionModel()

  pdm.addPointSet([
      (0, 0, 0), 
      (100, 0, 0), 
      (200, 0, 0),
      (300, 0, 0),
      (400, 0, 0),
      (500, 0, 0),
      ])
  pdm.addPointSet([
      (0, 0, 0), 
      (100, 0, 0), 
      (200, 0, 0),
      (300, 10, 0),
      (400, 0, 0),
      (500, 0, 0),
      ])
  pdm.addPointSet([
      (0, 10, 0), 
      (100, 10, 0), 
      (200, 10, 0),
      (300, 10, 0),
      (400, 10, 0),
      (500, 10, 0),
      ])
  
  pdm.addPointSet([
      (0, 0, 0), 
      (100, 0, 0), 
      (200, 0, 0),
      (300, 0, 0),
      (400, 0, 0),
      (500, 10, 0),
      ])
        

  pdm.procrustes()
  pdm.pca()
  pdm.variations()
  pdm.addActors(pdm.vertexGrids, 0)
  pdm.addActors(pdm.alignedGrids, 2)
  pdm.addActors(pdm.analyzedGrids, 4)
  pdm.addActors(pdm.meanShape, 6)
  pdm.visualizeMean()
  pdm.render()



if __name__ == '__main__':
  main()
