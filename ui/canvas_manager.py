import tkinter as tk

class CanvasManager:
    def __init__(self, parent):
        # Lienzo con las medidas exactas solicitadas: 900x600
        self.canvas = tk.Canvas(parent, width=900, height=600, bg="white", cursor="cross")
        
        # Variables para almacenar el primer clic del usuario
        self.start_x = None
        self.start_y = None
        
    def get_widget(self):
        """Retorna el widget de Tkinter para empaquetarlo en la ventana."""
        return self.canvas
        
    def draw_pixel(self, x, y, color="black"):
        """Tkinter no tiene un método nativo para pintar un solo pixel, 
        así que dibujamos un rectángulo de 1x1."""
        self.canvas.create_rectangle(x, y, x+1, y+1, fill=color, outline=color)
        
    def clear_canvas(self):
        """Limpia todos los dibujos del lienzo."""
        self.canvas.delete("all")