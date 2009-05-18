import colorsys
import logging

import vtk


def getColors(colors):
  """
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

    self.renderWindow = vtk.vtkRenderWindow()
    self.renderWindow.SetSize(300, 300)
    self.renderWindow.AddRenderer( self.renderer )
  
    # render window interactor
    self.windowInteractor = vtk.vtkRenderWindowInteractor()
    self.windowInteractor.SetRenderWindow(self.renderWindow)

    self.vertexGrids = []
    self.alignedGrids = []
    self.analyzedGrids = []

    self.colors = getColors(10)

  def addPointSet(self, data):
    """
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
    """
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
    """
    """

    logging.info("running procrustes")

    size = len(self.vertexGrids)

    self.filterGPA.SetNumberOfInputs(size)

    for id, grid in enumerate(self.vertexGrids):
      self.filterGPA.SetInput(id, grid)
      
    self.filterGPA.Update()

    for id in range(size):
      grid = self.filterGPA.GetOutput(id)
      self.alignedGrids.append(grid)
      
    logging.info("done")
  
  def pca(self):
    """
    """

    logging.info("running pca")

    size = len(self.alignedGrids)

    self.filterPCA.SetNumberOfInputs(size)
    
    for id, grid in enumerate(self.alignedGrids):    
      self.filterPCA.SetInput(id, grid)

    self.filterGPA.Update()

    for id in range(size):
      grid = self.filterPCA.GetOutput(id)
      self.analyzedGrids.append(grid)

    logging.info("done")

  def render(self):
    """
    """

    logging.info("rendering")
    
    self.renderWindow.Render()
    
    # initialize and start the interactor
    self.windowInteractor.Initialize()
    self.windowInteractor.Start()
    
    logging.info("done")


def main():
  logging.basicConfig(level=logging.DEBUG)
  pdm = PointDistributionModel()

  pdm.addPointSet([
      (0, 0, 0), 
      (3, 1, 0), 
      (2, 2, 0),
      ])
  
  pdm.addPointSet([
      (0.7, 0, 0), 
      (3.5, 1, 0), 
      (2.3, 2, 0),
      ])

  pdm.procrustes()
  pdm.pca()
  pdm.addActors(pdm.vertexGrids, 0)
  pdm.addActors(pdm.alignedGrids, 2)
  pdm.addActors(pdm.analyzedGrids, 4)
  pdm.render()

if __name__ == '__main__':
  main()
