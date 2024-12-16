import gdspy
import numpy as np

# Parametry
size_of_cell = 0.5  
layer_num = 1
radius = 2

lib = gdspy.GdsLibrary()

unitCell = lib.new_cell('CELL')

angles = np.linspace(0, 2 * np.pi, 10, endpoint=False)[1:]  # Pomijamy środek (kąt 0)
for angle in angles:
    c_x = radius * np.cos(angle)
    c_y = radius * np.sin(angle)
    unitCell.add(gdspy.Rectangle((c_x - 1, c_y - 1), (c_x + 1, c_y + 1), layer=layer_num))

grid = lib.new_cell("GRID")
grid.add(gdspy.CellReference(unitCell, origin=(0, 0), magnification=size_of_cell))

lib.write_gds("image.gds")
