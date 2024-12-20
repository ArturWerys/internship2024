import gdspy
from PIL import Image
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import time
import numpy as np


def draw_circle(library, cell_name, radius=1, size_of_cell=2, layer_number=1, x_px=0, y_px=0):
    center_x = x_px * size_of_cell
    center_y = - y_px * size_of_cell
    circle = gdspy.Round((center_x, center_y), radius, layer=layer_number)
    cell_name.add(circle)
    library.write_gds("image.gds")


Tk().withdraw()

filepath = askopenfilename(title="Wybierz plik obrazu", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])

if filepath:

    image = Image.open(filepath)
    lib = gdspy.GdsLibrary()
    cell_name = lib.new_cell(f"Cell_{int(time.time())}")  # Dodanie znacznika czasu

    print(f"Obraz wczytany: {filepath}")

    x, y = image.size

    pixels = []
    radii = []

    for i in range(x):
        for j in range(y):

            pixel = image.getpixel((i, j))
            pixels.append(pixel)

            print(f"Wartość piksela: {pixel}")

            r_max = int(np.sqrt(max(pixels) / np.pi))
            r_min = int(np.sqrt(min(pixels) / np.pi))

            if r_min < 1:
                r_min = 1

            radii.append(r_min)
            radii.append(r_max)

            radius_range = r_max - r_min

            print(r_min)
            print(r_max)

            size_of_cell = r_max

            area_min = np.pi * (r_min ** 2)
            area_max = np.pi * (r_max ** 2)

            if pixel > 0:
                area = area_min + (pixel / 255) * (area_max - area_min)
                r_new = np.sqrt(area / np.pi)
                radii.append(r_new)
            else:
                r_new = 0

            if r_new > 0:
                draw_circle(lib, cell_name, r_new, size_of_cell, layer_number=1, x_px=i, y_px=j)

else:
    print("Nie wybrano pliku.")
