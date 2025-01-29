import gdspy
from PIL import Image
import numpy as np
import time
from tqdm import tqdm
import argparse


def draw_circle(cell, radius=1, size_of_cell=2, layer_number=1, x_px=0, y_px=0):
    """Draws a circle in the given cell."""
    center_x = x_px * size_of_cell
    center_y = -y_px * size_of_cell
    circle = gdspy.Round((center_x, center_y), radius, layer=layer_number)
    cell.add(circle)


def draw_square(cell, side_length=1, size_of_cell=2, layer_number=1, x_px=0, y_px=0):
    """Draws a square in the given cell."""
    x1 = x_px * size_of_cell - side_length / 2
    y1 = y_px * size_of_cell - side_length / 2
    x2 = x_px * size_of_cell + side_length / 2
    y2 = y_px * size_of_cell + side_length / 2

    square = gdspy.Rectangle((x1, y1), (x2, y2), layer=layer_number)
    cell.add(square)


def draw_pentagon(cell, side_length=1, size_of_cell=2, layer_number=1, x_px=0, y_px=0):
    """Draws a pentagon in the given cell."""
    center_x = x_px * size_of_cell
    center_y = -y_px * size_of_cell
    angle = 2 * np.pi / 5  #
    points = [
        (center_x + side_length * np.cos(i * angle), center_y + side_length * np.sin(i * angle))
        for i in range(5)
    ]
    pentagon = gdspy.Polygon(points, layer=layer_number)
    cell.add(pentagon)


def draw_hexagon(cell, side_length=1, size_of_cell=2, layer_number=1, x_px=0, y_px=0):
    """Draws a hexagon in the given cell."""
    center_x = x_px * size_of_cell
    center_y = -y_px * size_of_cell
    angle = np.pi / 3
    points = [
        (center_x + side_length * np.cos(i * angle), center_y + side_length * np.sin(i * angle))
        for i in range(6)
    ]
    hexagon = gdspy.Polygon(points, layer=layer_number)
    cell.add(hexagon)


def draw_triangle(cell, side_length=1, size_of_cell=2, layer_number=1, x_px=0, y_px=0):
    """Draws an equilateral triangle in the given cell."""
    center_x = x_px * size_of_cell
    center_y = -y_px * size_of_cell
    height = np.sqrt(3) / 2 * side_length
    points = [
        (center_x, center_y + 2 * height / 3),
        (center_x - side_length / 2, center_y - height / 3),
        (center_x + side_length / 2, center_y - height / 3),
    ]
    triangle = gdspy.Polygon(points, layer=layer_number)
    cell.add(triangle)


def draw_star(cell, inner_radius=100, outer_radius=500, size_of_cell=1000, arms=7, offset_angle=0, layer_number=1, x_px=0, y_px=0):
    """Draws a star in the given cell."""
    center_x = x_px * size_of_cell
    center_y = -y_px * size_of_cell
    points = []
    for arm in range(0,arms*2,2):
        points.append((center_x + outer_radius*np.cos(np.deg2rad(360/arms/2*arm+offset_angle)), center_y + outer_radius*np.sin(np.deg2rad(360/arms/2*arm+offset_angle))))
        points.append((center_x + inner_radius*np.cos(np.deg2rad(360/arms/2*(arm+1)+offset_angle)), center_y + inner_radius*np.sin(np.deg2rad(360/arms/2*(arm+1)+offset_angle))))
    star = gdspy.Polygon(points, layer=layer_number)
    cell.add(star)


def process_image(filepath, size_of_cell, r_min, r_max, shape, excluded):
    """Processes the image and generates the GDS file."""

    image = Image.open(filepath)
    lib = gdspy.GdsLibrary(unit=1e-9)
    cell = lib.new_cell(f"Cell_{int(time.time())}")

    print(f"Loaded image: {filepath}")
    np_data = np.asarray(image)

    total_pixels = len(np_data) * len(np_data[0])

    # Konwersja na liczbę
    excluded = set(map(int, excluded))

    if shape == 0:  # Circle

        with tqdm(total=total_pixels, desc="Drawing Circles", ncols=80) as pbar:
            for i in range(len(np_data)):
                for j in range(len(np_data[i])):
                    pixel = np_data[i][j]

                    if pixel in excluded:
                        pbar.update(1)
                        continue

                    area_min = np.pi * (r_min ** 2)
                    area_max = np.pi * (r_max ** 2)

                    if pixel >= 0:
                        area = area_min + (pixel / 255) * (area_max - area_min)
                        r_new = np.sqrt(area / np.pi)
                    else:
                        r_new = 0

                    if r_new > 0:
                        draw_circle(cell, r_new, size_of_cell, layer_number=1, x_px=i, y_px=j)

                    pbar.update(1)
    elif shape == 1:  # Triangle

        side_min = r_min
        side_max = r_max

        if side_min < 1:
            side_min = 1

        with tqdm(total=total_pixels, desc="Drawing Triangles", ncols=80) as pbar:
            for i in range(len(np_data)):
                for j in range(len(np_data[i])):
                    pixel = np_data[i][j]

                    if pixel in excluded:
                        pbar.update(1)
                        continue

                    if pixel >= 0:
                        side_length = side_min + (pixel / 255) * (side_max - side_min)
                        draw_triangle(cell, side_length, size_of_cell=size_of_cell, layer_number=1, x_px=i, y_px=j)
                        pbar.update(1)

    elif shape == 2:  # Square

        side_min = r_min
        side_max = r_max

        if side_min < 1:
            side_min = 1

        with tqdm(total=total_pixels, desc="Drawing Squares", ncols=80) as pbar:
            for i in range(len(np_data)):
                for j in range(len(np_data[i])):
                    pixel = np_data[i][j]

                    if pixel in excluded:
                        pbar.update(1)
                        continue

                    if pixel >= 0:
                        side_length = side_min + (pixel / 255) * (side_max - side_min)
                        draw_square(cell, side_length, size_of_cell=size_of_cell, layer_number=1, x_px=i, y_px=j)
                        pbar.update(1)

    elif shape == 3:  # Pentagon

        side_min = r_min
        side_max = r_max

        if side_min < 1:
            side_min = 1

        with tqdm(total=total_pixels, desc="Drawing Pentagons", ncols=80) as pbar:
            for i in range(len(np_data)):
                for j in range(len(np_data[i])):
                    pixel = np_data[i][j]

                    if pixel in excluded:
                        pbar.update(1)
                        continue

                    if pixel >= 0:
                        side_length = side_min + (pixel / 255) * (side_max - side_min)
                        draw_pentagon(cell, side_length, size_of_cell=size_of_cell, layer_number=1, x_px=i, y_px=j)
                        pbar.update(1)

    elif shape == 4:  # Hexagon

        side_min = r_min
        side_max = r_max

        if side_min < 1:
            side_min = 1

        with tqdm(total=total_pixels, desc="Drawing Hexagons", ncols=80) as pbar:
            for i in range(len(np_data)):
                for j in range(len(np_data[i])):
                    pixel = np_data[i][j]

                    if pixel in excluded:
                        pbar.update(1)
                        continue

                    if pixel >= 0:
                        side_length = side_min + (pixel / 255) * (side_max - side_min)
                        draw_hexagon(cell, side_length, size_of_cell=size_of_cell, layer_number=1, x_px=i, y_px=j)
                        pbar.update(1)

    elif shape == 5:  # Star
        with tqdm(total=total_pixels, desc="Drawing Stars", ncols=80) as pbar:
            for i in range(len(np_data)):
                for j in range(len(np_data[i])):
                    pixel = np_data[i][j]

                    if pixel in excluded:
                        pbar.update(1)
                        continue

                    area_min = np.pi * (r_min ** 2)
                    area_max = np.pi * (r_max ** 2)

                    if pixel >= 0:
                        area = area_min + (pixel / 255) * (area_max - area_min)
                        r_new = np.sqrt(area / np.pi)
                    else:
                        r_new = 0

                    if r_new > 0:
                        draw_star(cell, inner_radius=r_new, size_of_cell=size_of_cell, layer_number=1, x_px=i, y_px=j)
                    pbar.update(1)
    
    else:
        print("Invalid input. Exiting.")
        return

    lib.write_gds("image.gds")
    print("GDS file created: image.gds")


def main():
    """Parsing arguments from the terminal and starting image processing."""
    parser = argparse.ArgumentParser(description="Processes an image and generates a GDS file.")

    parser.add_argument("filepath", type=str, help="Path to the image file")
    parser.add_argument("size_of_cell", type=int, help="Size of cell")
    parser.add_argument("r_min", type=int, help="Minimum radius/side length")
    parser.add_argument("r_max", type=int, help="Maximum radius/side length")
    parser.add_argument("shape", type=int, choices=range(6),
                        help="Shape: 0=Circle, 1=Triangle, 2=Square, 3=Pentagon, 4=Hexagon, 5=Star")
    parser.add_argument("excluded", nargs='*', help="Pixels to exclude (separated by spaces)")

    args = parser.parse_args()

    process_image(args.filepath, args.size_of_cell, args.r_min, args.r_max, args.shape, args.excluded)

    print("Zespół najlepszych praktykantów Werys/Głażewski sp. z o.o. życzy miłego dnia! :)")


if __name__ == "__main__":
    main()
