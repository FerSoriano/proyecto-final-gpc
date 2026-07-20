
from algorithms import lineas

def main():
    # Test DDA
    dda_instance = lineas.DDA(3, 5, 17, 23)
    print(dda_instance)
    dda_instance.print_points()

    # Test Bresenham
    bresenham_instance = lineas.Bresenham(19, 0, 0, 13)
    print(bresenham_instance)
    bresenham_instance.print_points()

if __name__ == "__main__":
    main()