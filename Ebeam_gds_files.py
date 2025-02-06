from GDS_shape_generator import process_image as pi
import time
# Pierwsza soczewka
pi("", "pow_1.gds", 1600, 400, 800, 2, [])


time.sleep(1)

# Druga soczewka
pi("", "pow_1_neg.gds", 1600, 400, 800, 3, [])
