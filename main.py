
from algorithms import lineas

from ui.main_window import MainWindow
from controllers.app_controller import AppController

def test_algorithms():
    # Test DDA
    dda_instance = lineas.DDA(3, 5, 17, 23)
    print(dda_instance)
    dda_instance.print_points()

    # Test Bresenham
    bresenham_instance = lineas.Bresenham(19, 0, 0, 13)
    print(bresenham_instance)
    bresenham_instance.print_points()

def main():
    # Inicializamos la ventana principal (la vista)
    app = MainWindow()
    
    # Inicializamos el controlador inyectándole la vista
    controller = AppController(app)
    
    # Arrancamos el mainloop de Tkinter
    app.mainloop()

if __name__ == "__main__":
    main()