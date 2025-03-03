from GDS_shape_generator import process_image as pimg
import time
from Diffraction_Grating import generate_gds_file as gds

# Pierwsza soczewka
pimg("C:\Programowanie\MatLab\Cezamat\lens1.png", "pow_1.gds", 1600, 400, 800, 2, [])
time.sleep(1)
# r min > 200

# Druga soczewka
pimg("C:\Programowanie\MatLab\Cezamat\lens1_neg.png", "pow_1_neg.gds", 1600, 400, 800, 3, [])
time.sleep(1)

# Generacja siatek dyfrakcyjnych
gds("Dif_Grat_3_8.gds",1,25,3,1,8)
time.sleep(1)

gds("Dif_Grat_2_7.gds",1,30,2,1,7)
time.sleep(1)

gds("Dif_Grat_0_7_20.gds",1,70,0.7,1,20)