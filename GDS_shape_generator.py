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


def draw_square(library, cell, size_of_cell=2, layer_number=1, x_px=0, y_px=0):
    # Wyznaczenie współrzędnych rogu kwadratu
    x1 = x_px * size_of_cell
    y1 = y_px * size_of_cell

    # Długość boku kwadratu
    x2 = x1 + size_of_cell
    y2 = y1 + size_of_cell

    # Tworzenie kwadratu (Rectangle od (x1, y1) do (x2, y2))
    square = gdspy.Rectangle((x1, y1), (x2, y2), layer=layer_number)

    # Dodanie kwadratu do komórki
    cell.add(square)

    # Zapis biblioteki do pliku GDS
    library.write_gds("image.gds")


Tk().withdraw()

filepath = askopenfilename(title="Wybierz plik obrazu", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])

if filepath:

    image = Image.open(filepath)

    lib = gdspy.GdsLibrary()
    cell_name = lib.new_cell(f"Cell_{int(time.time())}")  # Dodanie znacznika czasu

    print(f"Obraz wczytany: {filepath}")

    x, y = image.size

    np_data = np.asarray(image)
    print(np_data)

    question = int(input("Circle / Square [ 0 / 1 ]: "))

    if question == 0:
        print("circle")

        radii = []

        for i in range(len(np_data)):
            for j in range(len(np_data[i])):

                pixel = np_data[i][j]
                print("Wartość iterowanego pixela: ", pixel)

                max_pixel = np.amax(np_data)
                min_pixel = np.amin(np_data)

                print(max_pixel)
                print(min_pixel)

                print("--------------")

                r_max = int(np.sqrt(max_pixel / np.pi))
                r_min = int(np.sqrt(min_pixel / np.pi))

                if r_min < 1:
                    r_min = 1

                radii.append(r_min)
                radii.append(r_max)

                radius_range = r_max - r_min

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

    elif question == 1:

        # Do skończenia, to nie działa jak powinno, wersja niekompletna

        print("square")

        for i in range(len(np_data)):
            for j in range(len(np_data[i])):

                pixel = np_data[i][j]
                print("Wartość iterowanego pixela: ", pixel)

                max_pixel = np.amax(np_data)
                min_pixel = np.amin(np_data)

                area_min = max_pixel * max_pixel
                area_max = min_pixel * min_pixel

                area = area_min + (pixel / 255) * (area_max - area_min)

                draw_square(lib, cell_name, size_of_cell=1, layer_number=1, x_px=1, y_px=1)

    else:
        print("Invalid number")

else:
    print("Nie wybrano pliku.")
