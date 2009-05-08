# File:        sphere2.py

# import python module
import vtk

# our data source, a PolyDataReader
reader = vtk.vtkPolyDataReader()
reader.SetFileName("H:/desktop/sphere.vtk")
reader.Update() # by calling Update() we read the file

# find the range of the point scalars
pa,pb = reader.GetOutput().GetPointData().GetScalars().GetRange()
pnm =  reader.GetOutput().GetPointData().GetScalars().GetName()
print "Range of %s: %4.2f-%4.2f" %(pnm,pa,pb)

# ...and of the cell scalars
ca,cb = reader.GetOutput().GetCellData().GetScalars().GetRange()
cnm =  reader.GetOutput().GetCellData().GetScalars().GetName()
print "Range of %s: %4.2f-%4.2f" %(cnm,ca,cb)

# transfer function (lookup table) for mapping point scalar data
# to colors (parent class is vtkScalarsToColors)
lut = vtk.vtkColorTransferFunction()
lut.AddRGBPoint(pa,           0.0, 0.0, 1.0)
lut.AddRGBPoint(pa+(pb-pa)/4, 0.0, 0.5, 0.5)
lut.AddRGBPoint(pa+(pb-pa)/2, 0.0, 1.0, 0.0)
lut.AddRGBPoint(pb-(pb-pa)/4, 0.5, 0.5, 0.0)
lut.AddRGBPoint(pb,           1.0, 0.0, 0.0)

# glyphs for vector data
glyphs = vtk.vtkGlyph3D()
glyphs.SetInput(reader.GetOutput())
arrow = vtk.vtkArrowSource() # the geometry used
arrow.SetTipRadius(.05)
arrow.SetShaftRadius(.025)
glyphs.SetSource(0,arrow.GetOutput())
glyphs.SetVectorModeToUseVector()     # use vector magnitude
glyphs.SetScaleModeToScaleByVector()  # for scaling 
glyphs.SetScaleFactor(0.5)            # global scaling
glyphs.SetColorModeToColorByScalar()  # color by point scalars
glyphMapper = vtk.vtkPolyDataMapper()
glyphMapper.SetLookupTable(lut)
glyphMapper.SetInput(glyphs.GetOutput())
glyphActor = vtk.vtkActor()
glyphActor.SetMapper(glyphMapper)

# lookup table for cell data
lut2 = vtk.vtkLookupTable()
lut2.SetHueRange(0.667, 0.667)
lut2.SetSaturationRange(0.0, 1.0)
lut2.SetValueRange(0.8, 1.0)
lut2.SetAlphaRange(1.0, 0.2)
lut2.SetTableRange(ca,cb)

# we want to use transparency here, then we need to sort polygons
# to get it correct
sorter = vtk.vtkDepthSortPolyData()
sorter.SetInput(reader.GetOutput())
# ...and then we need a camera to get a direction to depth sort in
camera = vtk.vtkCamera()
sorter.SetCamera(camera)

# mapper
mapper = vtk.vtkPolyDataMapper()
mapper.SetLookupTable(lut2)
mapper.SetScalarRange(ca,cb);
mapper.SetInput(sorter.GetOutput())
# here we use the cell data
mapper.SetScalarModeToUseCellData()

# the actor
myActor = vtk.vtkActor()
myActor.SetMapper( mapper )

# a colorbar for point scalars
scalarBar = vtk.vtkScalarBarActor()
scalarBar.SetLookupTable( lut )
scalarBar.SetTitle("Point scalar value")
scalarBar.SetOrientationToHorizontal()
scalarBar.GetLabelTextProperty().SetColor(0,0,1)
scalarBar.GetTitleTextProperty().SetColor(0,0,1)

# position it in window
coord1 = scalarBar.GetPositionCoordinate()
coord1.SetCoordinateSystemToNormalizedViewport()
coord1.SetValue(0.1,0.05)
scalarBar.SetWidth(.8)
scalarBar.SetHeight(.15)

# another colorbar for cell scalars
scalarBar2 = vtk.vtkScalarBarActor()
scalarBar2.SetLookupTable( mapper.GetLookupTable() )
scalarBar2.SetTitle("Cell scalar value")
scalarBar2.SetOrientationToHorizontal()
scalarBar2.GetLabelTextProperty().SetColor(0,0,1)
scalarBar2.GetTitleTextProperty().SetColor(0,0,1)

# position it in window
coord2 = scalarBar2.GetPositionCoordinate()
coord2.SetCoordinateSystemToNormalizedViewport()
coord2.SetValue(0.1,0.85)
scalarBar2.SetWidth(.8)
scalarBar2.SetHeight(.15)

# renderer and render window 
ren = vtk.vtkRenderer()
ren.SetBackground(1, 1, 1)
renWin = vtk.vtkRenderWindow()
renWin.SetSize(512, 512)
renWin.AddRenderer( ren )

# render window interactor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow( renWin )

# add the actors to the renderer
ren.AddActor( glyphActor )
ren.AddActor( myActor )
ren.AddActor( scalarBar )
ren.AddActor( scalarBar2 )
ren.SetActiveCamera(camera) # add camera
ren.ResetCamera()

# render
renWin.Render()

# initialize and start the interactor
iren.Initialize()
iren.Start()
