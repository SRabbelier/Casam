# Directory containing class headers.
SET(VTK_INFOVIS_HEADER_DIR "${VTK_INSTALL_PREFIX}/include/vtk-5.2")

# Classes in vtkInfovis.
SET(VTK_INFOVIS_CLASSES
  "vtkArrayMap"
  "vtkAssignCoordinates"
  "vtkBoxLayoutStrategy"
  "vtkChacoGraphReader"
  "vtkCircularLayoutStrategy"
  "vtkClustering2DLayoutStrategy"
  "vtkCommunity2DLayoutStrategy"
  "vtkConstrained2DLayoutStrategy"
  "vtkDataObjectToTable"
  "vtkDelimitedTextReader"
  "vtkEdgeCenters"
  "vtkExtractSelectedGraph"
  "vtkFast2DLayoutStrategy"
  "vtkFixedWidthTextReader"
  "vtkForceDirectedLayoutStrategy"
  "vtkGraphHierarchicalBundle"
  "vtkGraphLayout"
  "vtkGraphLayoutStrategy"
  "vtkGraphMapper"
  "vtkGraphToPolyData"
  "vtkGroupLeafVertices"
  "vtkISIReader"
  "vtkInteractorStyleTreeMapHover"
  "vtkLabeledTreeMapDataMapper"
  "vtkMergeColumns"
  "vtkMergeTables"
  "vtkPassThrough"
  "vtkPassThroughLayoutStrategy"
  "vtkPruneTreeFilter"
  "vtkRISReader"
  "vtkRandomGraphSource"
  "vtkRandomLayoutStrategy"
  "vtkSimple2DLayoutStrategy"
  "vtkSliceAndDiceLayoutStrategy"
  "vtkSquarifyLayoutStrategy"
  "vtkStringToCategory"
  "vtkStringToNumeric"
  "vtkTableToGraph"
  "vtkTableToTreeFilter"
  "vtkThresholdTable"
  "vtkTimePointUtility"
  "vtkTreeFieldAggregator"
  "vtkTreeLayoutStrategy"
  "vtkTreeOrbitLayoutStrategy"
  "vtkTreeLevelsFilter"
  "vtkTreeMapLayout"
  "vtkTreeMapLayoutStrategy"
  "vtkTreeMapToPolyData"
  "vtkTreeMapViewer"
  "vtkTulipReader"
  "vtkVertexDegree"
  "vtkViewTheme"
  "vtkXMLTreeReader"
  "vtkSQLGraphReader"
  "vtkStringToTimePoint"
  "vtkTimePointToString")

# Abstract classes in vtkInfovis.
SET(VTK_INFOVIS_CLASSES_ABSTRACT
  "vtkGraphLayoutStrategy"
  "vtkTreeMapLayoutStrategy")

# Wrap-exclude classes in vtkInfovis.
SET(VTK_INFOVIS_CLASSES_WRAP_EXCLUDE)

# Set convenient variables to test each class.
FOREACH(class ${VTK_INFOVIS_CLASSES})
  SET(VTK_CLASS_EXISTS_${class} 1)
ENDFOREACH(class)
FOREACH(class ${VTK_INFOVIS_CLASSES_ABSTRACT})
  SET(VTK_CLASS_ABSTRACT_${class} 1)
ENDFOREACH(class)
FOREACH(class ${VTK_INFOVIS_CLASSES_WRAP_EXCLUDE})
  SET(VTK_CLASS_WRAP_EXCLUDE_${class} 1)
ENDFOREACH(class)
