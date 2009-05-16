# Directory containing class headers.
SET(VTK_PARALLEL_HEADER_DIR "${VTK_INSTALL_PREFIX}/include/vtk-5.2")

# Classes in vtkParallel.
SET(VTK_PARALLEL_CLASSES
  "vtkBranchExtentTranslator"
  "vtkCollectGraph"
  "vtkCollectPolyData"
  "vtkCollectTable"
  "vtkCommunicator"
  "vtkCompositer"
  "vtkCompressCompositer"
  "vtkCutMaterial"
  "vtkDistributedDataFilter"
  "vtkDistributedStreamTracer"
  "vtkDummyCommunicator"
  "vtkDummyController"
  "vtkDuplicatePolyData"
  "vtkEnSightWriter"
  "vtkExtractCTHPart"
  "vtkExtractPiece"
  "vtkExtractPolyDataPiece"
  "vtkExtractUnstructuredGridPiece"
  "vtkExtractUserDefinedPiece"
  "vtkMemoryLimitImageDataStreamer"
  "vtkMultiProcessController"
  "vtkParallelFactory"
  "vtkPassThroughFilter"
  "vtkPCellDataToPointData"
  "vtkPChacoReader"
  "vtkPDataSetReader"
  "vtkPDataSetWriter"
  "vtkPExtractArraysOverTime"
  "vtkPieceRequestFilter"
  "vtkPieceScalars"
  "vtkPImageWriter"
  "vtkPKdTree"
  "vtkPLinearExtrusionFilter"
  "vtkPOPReader"
  "vtkPOutlineCornerFilter"
  "vtkPOutlineFilter"
  "vtkPPolyDataNormals"
  "vtkPProbeFilter"
  "vtkProcessGroup"
  "vtkProcessIdScalars"
  "vtkPSphereSource"
  "vtkPStreamTracer"
  "vtkRectilinearGridOutlineFilter"
  "vtkRTAnalyticSource"
  "vtkSocketCommunicator"
  "vtkSocketController"
  "vtkSubCommunicator"
  "vtkSubGroup"
  "vtkTemporalFractal"
  "vtkTemporalInterpolatedVelocityField"
  "vtkTemporalStreamTracer"
  "vtkTransmitImageDataPiece"
  "vtkTransmitPolyDataPiece"
  "vtkTransmitRectilinearGridPiece"
  "vtkTransmitStructuredGridPiece"
  "vtkTransmitUnstructuredGridPiece"
  "vtkXMLPHierarchicalBoxDataWriter"
  "vtkXMLPMultiBlockDataWriter"
  "vtkCompositeRenderManager"
  "vtkPipelineSize"
  "vtkParallelRenderManager"
  "vtkTreeCompositer"
  "vtkExodusIIWriter")

# Abstract classes in vtkParallel.
SET(VTK_PARALLEL_CLASSES_ABSTRACT
  "vtkCommunicator"
  "vtkMultiProcessController"
  "vtkPStreamTracer"
  "vtkParallelRenderManager")

# Wrap-exclude classes in vtkParallel.
SET(VTK_PARALLEL_CLASSES_WRAP_EXCLUDE)

# Set convenient variables to test each class.
FOREACH(class ${VTK_PARALLEL_CLASSES})
  SET(VTK_CLASS_EXISTS_${class} 1)
ENDFOREACH(class)
FOREACH(class ${VTK_PARALLEL_CLASSES_ABSTRACT})
  SET(VTK_CLASS_ABSTRACT_${class} 1)
ENDFOREACH(class)
FOREACH(class ${VTK_PARALLEL_CLASSES_WRAP_EXCLUDE})
  SET(VTK_CLASS_WRAP_EXCLUDE_${class} 1)
ENDFOREACH(class)
