
from algorithms import dda

def main():
    # Test DDA
    dda_instance = dda.DDA(3, 5, 17, 23)
    print(dda_instance)
    dda_instance.print_points()

if __name__ == "__main__":
    main()