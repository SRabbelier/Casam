import colorsys
import logging

import vtk

from casam.logic import pdmoverlay

class PointDistributionModel(object):
  """Calculates the Point Distribution Model using an unstructured grid
  """
  
  def __init__(self):
    """
    """
     
    self.filterGPA = vtk.vtkProcrustesAlignmentFilter()
    self.filterPCA = vtk.vtkPCAAnalysisFilter()
    
    self.vertexGrids = []
    self.alignedGrids = []
    self.analyzedGrids = []
    self.meanShape = [] 
    self.meanPositions = []
    self.variationPositions = []

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
    
    #Now let's get mean ^^
    b = vtk.vtkFloatArray()
    b.SetNumberOfComponents(0)
    b.SetNumberOfTuples(0)
    mean = vtk.vtkUnstructuredGrid()
    mean.DeepCopy(self.alignedGrids[0])
    #Get the mean shape:
    self.filterPCA.GetParameterisedShape(b, mean)
    self.meanShape.append(mean)   
    
    #get the meanpositions
    for pos in range(self.meanShape[0].GetNumberOfCells()):
      bounds = self.meanShape[0].GetCell(pos).GetBounds()
      self.meanPositions.append((bounds[0],bounds[2]))
      
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
       
    for pos in range (self.analyzedGrids[0].GetNumberOfCells()):
      for i in range(0,4):
        bounds = self.analyzedGrids[i].GetCell(pos).GetBounds()
        self.variationPositions.append((bounds[0],bounds[2]))
  
def makePDM():
  """Create the Point Distribution Model
  """
  logging.basicConfig(level=logging.DEBUG)
  
  pdm = PointDistributionModel()
  return pdm
