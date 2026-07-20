import tkinter as tk
from algorithms.lineas import DDA, Bresenham

class AppController:
    def __init__(self, view):
        self.view = view
        self.canvas_manager = self.view.canvas_manager
        
        # Estado de la aplicación
        self.current_mode = None  
        self.start_x = None
        self.start_y = None
        self.current_color = "black"  # Color por defecto

        # 1. Conectar botones de herramientas
        self.view.btn_dda.config(command=lambda: self.set_mode("DDA"))
        self.view.btn_bresenham.config(command=lambda: self.set_mode("BRESENHAM"))
        self.view.btn_clear.config(command=self.clear_canvas)

        # 2. Conectar la selección de colores del menú superior
        for color_name, square_widget in self.view.color_squares.items():
            # c=color_name asegura que se pase el color correcto en la función lambda
            square_widget.bind("<Button-1>", lambda event, c=color_name: self.set_color(c))

        # 3. Conectar el lienzo
        self.canvas_manager.canvas.bind("<Button-1>", self.on_canvas_click)

    def set_color(self, color):
        """Actualiza el color activo para los siguientes trazos."""
        self.current_color = self.view.colores[color]
        self.view.log_calculation(f"--- Color cambiado a: {color} ---")

    def set_mode(self, mode):
        self.current_mode = mode
        self.view.log_calculation(f"--- Modo seleccionado: {mode} ---")
        self.start_x = None
        self.start_y = None

    def clear_canvas(self):
        self.canvas_manager.clear_canvas()
        self.view.clear_log()
        self.view.log_calculation("--- Pantalla y registro limpios ---")
        self.start_x = None
        self.start_y = None

    def on_canvas_click(self, event):
        if not self.current_mode:
            self.view.log_calculation("Selecciona primero una primitiva para dibujar.")
            return

        if self.start_x is None and self.start_y is None:
            self.start_x = event.x
            self.start_y = event.y
            self.view.log_calculation(f"Punto inicial (x1, y1): ({self.start_x}, {self.start_y})")
        else:
            end_x = event.x
            end_y = event.y
            self.view.log_calculation(f"Punto final (x2, y2): ({end_x}, {end_y})")
            
            self.draw_primitive(self.start_x, self.start_y, end_x, end_y)
            
            self.start_x = None
            self.start_y = None

    def draw_primitive(self, x1, y1, x2, y2):
        points = []
        
        if self.current_mode == "DDA":
            alg = DDA(x1, y1, x2, y2)
            points = alg.generate_points()
        elif self.current_mode == "BRESENHAM":
            alg = Bresenham(x1, y1, x2, y2)
            points = alg.generate_points()

        self.view.log_calculation(f"Calculando {self.current_mode}...")
        
        for p in points:
            # Ahora le pasamos el color actual al método que pinta el pixel
            self.canvas_manager.draw_pixel(p[0], p[1], color=self.current_color)
            self.view.log_calculation(f"X: {p[0]}, Y: {p[1]}")
        
        self.view.log_calculation("--- Trazo finalizado ---\n")