import gdspy
import argparse
import math
import time

def calculate_growth_factor(period, max_spacing):
    num_steps = math.ceil(math.log(max_spacing / period) / math.log(1.5))
    return (max_spacing / period) ** (1 / max(1, num_steps))


def draw_variable_grating_lines(cell, period, depth, size_of_cell, layer_number, x_px, y_px, growth_factor):
    """Generates a linear diffraction grating with variable spacing."""
    start_x = x_px * size_of_cell * 1000
    start_y = -y_px * size_of_cell * 1000
    x_offset = start_x

    i = 0
    while x_offset < start_x + size_of_cell * 1000:
        line = gdspy.Rectangle((x_offset, start_y), (x_offset + depth * 1000, start_y + size_of_cell * 1000), layer=layer_number)
        cell.add(line)
        x_offset += period * (growth_factor ** i) * 1000
        if x_offset - start_x >= size_of_cell * 1000:
            break
        i += 1


def generate_gds_file(filename, grid_size, size_of_cell, period, amplitude, max_spacing):
    """Generates a GDS file with diffraction gratings."""
    growth_factor = calculate_growth_factor(period, max_spacing)
    lib = gdspy.GdsLibrary(unit=1e-9)
    cell = lib.new_cell(f"Grating_{int(1000 * time.time())}")

    for x in range(grid_size):
        for y in range(grid_size):
            draw_variable_grating_lines(cell, period, amplitude, size_of_cell, layer_number=1, x_px=x, y_px=y,
                                        growth_factor=growth_factor)

    lib.write_gds(filename)
    print(f"GDS file '{filename}' created successfully.")


def main():
    parser = argparse.ArgumentParser(description="Generate diffraction grating with variable spacing.")
    parser.add_argument("file", type=str, help="GDS file name")
    parser.add_argument("grid_size", type=int, help="Total grid size")
    parser.add_argument("size_of_cell", type=float, help="Size of each grid cell in µm")
    parser.add_argument("period", type=float, help="Base period of the grating in µm")
    parser.add_argument("amplitude", type=float, help="Amplitude/depth of grating in µm")
    parser.add_argument("max_spacing", type=float, help="Maximum spacing between lines in µm")

    args = parser.parse_args()
    generate_gds_file(args.file, args.grid_size, args.size_of_cell, args.period, args.amplitude, args.max_spacing)


if __name__ == "__main__":
    main()
