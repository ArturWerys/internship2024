import gdspy
from PIL import Image
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Python ma takie cos, co nazywa sie dictionary.
# To jest taka array, ktora przechowuje haslo i jego wartosc w parach.
# Przy definiowaniu funkcji to sie bardzo przydaje.
# Po pierwsze, mozecie podawac argumenty w dowolnej kolejnosci.
# Po drugie, mozecie je inicjalizowac z jakas wartoscia domyslna.
# Po trzecie, tych, ktore maja wartosc domyslna, nie musicie za kazdym razem podawac.
# To jest jak varargin w Matlabie, tylko znacznie lepsze.

# przyklad:
# def draw_circle(library,cell_name,radius=1,size_of_cell=2,layer_numer=1,x_px=0,y_px=0):
# i teraz mozecie wywolac funkcje np. tak:
    #def draw_circle(library,cell_name,radius=1,size_of_cell=2,layer_number=1,x_px=0,y_px=0):
# draw_circle(lib,main_cell,x_px=i,y_px=j)
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
    main_cell = lib.new_cell('Main') # zeby mi to dzialalo, za kazdym razem musze zmieniac te nazwe, bo inaczej jest error

    print(f"Obraz wczytany: {filepath}")
    x, y = image.size

# gdzies trzeba zdefiniowac:
# jaki wymiar ma piksel (czyli o ile skaczemy w petli)
# jaka jest srednica albo promien kolka dla minimalnej wartosci piksela
# jaka jest srednica albo promien kolka dla maksymalnej wartosci piksela
# pamietajcie, ze wartosc piksela ma byc proporcjonalna do powierzchni kola, a nie samego promienia (zeleznosc niekoniecznie bedzie liniowa)

    for i in range(x):
        for j in range(y):
            pixel = image.getpixel((i, j))
            print(f"Wartość piksela: {pixel}")

            layer = 11

            for ll in range(layer + 1):
                if ll <= 10:
                    if 0 + 25 * ll < pixel <= 25 + 25 * ll:
                        draw_circle(lib, main_cell, 1, 2, ll, i, j) # tu juz macie wszystko co trzeba, musicie tylko modyfikowac powierzchnie kolka zamiast warstwy

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
