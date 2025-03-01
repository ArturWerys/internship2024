import gdspy
import argparse


def draw_variable_grating_lines(cell, period, depth, size_of_cell, layer_number, x_px, y_px, growth_factor):
    """Generates a linear diffraction grating with variable spacing."""
    start_x = x_px * size_of_cell
    start_y = -y_px * size_of_cell
    x_offset = start_x

    i = 0
    while x_offset < start_x + size_of_cell:
        line = gdspy.Rectangle((x_offset, start_y), (x_offset + depth, start_y + size_of_cell), layer=layer_number)
        cell.add(line)
        i += 1
        x_offset += period * (growth_factor ** i)


def generate_gds_file(filename, grid_size, size_of_cell, period, amplitude,growth_factor):
    """Generates a GDS file with diffraction gratings."""
    lib = gdspy.GdsLibrary(unit=1e-9)
    cell = lib.new_cell("Grating")

    for x in range(grid_size):
        for y in range(grid_size):
            draw_variable_grating_lines(cell, period, amplitude, size_of_cell, layer_number=1, x_px=x, y_px=y, growth_factor=growth_factor)

    lib.write_gds(filename)
    print(f"GDS file '{filename}' created successfully.")


def main():
    parser = argparse.ArgumentParser(description="Generate diffraction grating with variable spacing.")
    parser.add_argument("file", type=str, help="GDS file name")
    parser.add_argument("grid_size", type=int, help="Total grid size")
    parser.add_argument("size_of_cell", type=float, help="Size of each grid cell")
    parser.add_argument("period", type=float, help="Base period of the grating")
    parser.add_argument("amplitude", type=float, help="Amplitude/depth of grating")
    parser.add_argument("growth_factor", type=float, help="Factor controlling the increase in spacing")

    args = parser.parse_args()
    generate_gds_file(args.file, args.grid_size, args.size_of_cell, args.period, args.amplitude,args.growth_factor)


if __name__ == "__main__":
    main()
