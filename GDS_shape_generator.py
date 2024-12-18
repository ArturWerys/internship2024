import gdspy
from PIL import Image
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def draw_circle(library, cell_name, radius, size_of_cell, layer_number, x_px, y_px):
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
    main_cell = lib.new_cell('Main')

    print(f"Obraz wczytany: {filepath}")
    x, y = image.size

    for i in range(x):
        for j in range(y):
            pixel = image.getpixel((i, j))
            print(f"Wartość piksela: {pixel}")

            layer = 11

            for ll in range(layer + 1):
                if ll <= 10:
                    if 0 + 25 * ll < pixel <= 25 + 25 * ll:
                        draw_circle(lib, main_cell, 1, 2, ll, i, j)

                # if l == 11 and not executed_once_for_11:
                #     draw_circle(lib, main_cell, 1, 2, 11, i, j)
                #     executed_once_for_11 = True

            # if 0 < pixel <= 25:
            #     draw_circle(lib, main_cell, 1, 2, 1, i, j)
            # elif 63 < pixel <= 127:
            #     draw_circle(lib, main_cell, 1, 2, 2, i, j)
            # elif 127 < pixel <= 191:
            #     draw_circle(lib, main_cell, 1, 2, 3, i, j)
            # elif 191 < pixel < 255:
            #     draw_circle(lib, main_cell, 1, 2, 4, i, j)

else:
    print("Nie wybrano pliku.")
