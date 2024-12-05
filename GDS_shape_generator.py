import gdspy
import numpy as np

sizeOfTheCell = 0.5
layerNum = 1
# The GDSII file is called a library, which contains multiple cells.
lib = gdspy.GdsLibrary()
gdspy.current_library = gdspy.GdsLibrary()

double_pi = 2*np.pi

# Geometry must be placed in cells.
unitCell = lib.new_cell('CELL')
square = gdspy.Rectangle((0.0, 0.0), (0.5, 0.5), layer=(int)(layerNum))
square2 = gdspy.Rectangle((0.5, 0.5), (1, 1), layer=(int)(2))

arc = gdspy.Round((0.5, 0.5), radius=0.25, initial_angle=0, final_angle=double_pi, layer=3)

unitCell.add(square)
unitCell.add(square2)
unitCell.add(arc)


grid = lib.new_cell("GRID")

scaledGrid = gdspy.CellReference(
    grid, origin=(0, 0), magnification=(float)(sizeOfTheCell))

top = lib.new_cell("TOP")
top.add(scaledGrid)
lib.write_gds("image.gds")