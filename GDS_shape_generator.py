import gdspy
from PIL import Image
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def draw_circle(library, cell_name, x_px, y_px):
    # Parametry
    size_of_cell = 1
    radius = 2

    center_x = x_px * size_of_cell
    center_y = - y_px * size_of_cell

    circle = gdspy.Round((center_x, center_y), radius, layer=2)
    cell_name.add(circle)
    library.write_gds("image.gds")


Tk().withdraw()

filepath = askopenfilename(title="Wybierz plik obrazu", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])

if filepath:
    image = Image.open(filepath)
    lib = gdspy.GdsLibrary()
    main_cell = lib.new_cell('Main')

    print(f"Obraz wczytany: {filepath}")
    x, y = image.size

    for i in range(x):
        for j in range(y):
            pixel = image.getpixel((i, j))
            print(f"Wartość piksela: {pixel}")
            draw_circle(lib, main_cell, i, j)

else:
    print("Nie wybrano pliku.")
