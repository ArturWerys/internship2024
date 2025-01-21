import gdspy
from PIL import Image
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np
import time
from tqdm import tqdm


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


def process_image(filepath):
    """Processes the image, asking the user to choose shape type, and generates the GDS file."""

    image = Image.open(filepath)
    lib = gdspy.GdsLibrary(unit=1e-9)
    cell = lib.new_cell(f"Cell_{int(time.time())}")

    print(f"Loaded image: {filepath}")
    np_data = np.asarray(image)

    size_of_cell = int(input("Size of cell: "))
    r_min = int(input("R min value: "))
    r_max = int(input("R max value: "))

    question = int(input("Circle / Square [ 0 / 1 ]: "))
    question2 = int(input("Zakres 0-254 / 1-255 [0/1]: "))

    total_pixels = len(np_data) * len(np_data[0])

    if question == 0:  # Circle

        with tqdm(total=total_pixels, desc="Drawing Circles", ncols=80) as pbar:
            for i in range(len(np_data)):
                for j in range(len(np_data[i])):
                    pixel = np_data[i][j]

                    area_min = np.pi * (r_min ** 2)
                    area_max = np.pi * (r_max ** 2)

                    if question2 == 0:
                        if pixel >= 0:
                            area = area_min + (pixel-1 / 254) * (area_max - area_min)
                            r_new = np.sqrt(area / np.pi)
                        else:
                            r_new = 0

                        if r_new > 0:
                            draw_circle(cell, r_new, size_of_cell, layer_number=1, x_px=i, y_px=j)
                    else:
                        if pixel > 1:
                            area = area_min + (pixel/ 255) * (area_max - area_min)
                            r_new = np.sqrt(area / np.pi)
                        else:
                            r_new = 0

                        if r_new > 0:
                            draw_circle(cell, r_new, size_of_cell, layer_number=1, x_px=i, y_px=j)

                    pbar.update(1)

    elif question == 1:  # Square

        print("Drawing squares...")
        side_min = r_min
        side_max = r_max

        if side_min < 1:
            side_min = 1

        with tqdm(total=total_pixels, desc="Drawing Squares", ncols=80) as pbar:
            for i in range(len(np_data)):
                for j in range(len(np_data[i])):

                    if question2 == 0:
                        pixel = np_data[i][j]
                        side_length = side_min + (pixel-1 / 254) * (side_max - side_min)
                        draw_square(cell, side_length, size_of_cell=size_of_cell, layer_number=1, x_px=i, y_px=j)

                    elif question2 == 1:

                        pixel = np_data[i][j]
                        side_length = side_min + (pixel / 255) * (side_max - side_min)
                        draw_square(cell, side_length, size_of_cell=size_of_cell, layer_number=1, x_px=i, y_px=j)

                    pbar.update(1)

    else:
        print("Invalid input. Exiting.")
        return

    lib.write_gds("image.gds")
    print("GDS file created: image.gds")


def main():
    Tk().withdraw()
    filepath = askopenfilename(title="Wybierz plik obrazu", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if filepath:
        process_image(filepath)
    else:
        print("No file selected.")
    print("Zespół najlepszych praktykantów Werys/Głażewski sp. z o.o. życzą miłego dnia! :)")


if __name__ == "__main__":
    main()
