import tkinter as tk

class CanvasManager:
    GRID_SPACING = 20
    GRID_COLOR_LIGHT = "#dddddd"
    GRID_COLOR_DARK = "#3a3a3a"
    BG_LIGHT = "white"
    BG_DARK = "#1e1e1e"

    def __init__(self, parent):
        # Lienzo con las medidas exactas solicitadas: 900x600
        self.canvas = tk.Canvas(parent, width=900, height=600, bg="white", cursor="cross")

        # Variables para almacenar el primer clic del usuario
        self.start_x = None
        self.start_y = None

    def get_widget(self):
        """Retorna el widget de Tkinter para empaquetarlo en la ventana."""
        return self.canvas

    def draw_pixel(self, x, y, color="black", size=1):
        """Tkinter no tiene un método nativo para pintar un solo pixel,
        así que dibujamos un rectángulo de tamaño `size`."""
        self.canvas.create_rectangle(x, y, x + size, y + size, fill=color, outline=color)

    def clear_canvas(self):
        """Limpia todos los dibujos del lienzo."""
        self.canvas.delete("all")

    def draw_grid(self, dark_mode=False):
        """Dibuja una cuadrícula de fondo (ayuda visual, no una primitiva educativa)."""
        width = int(self.canvas["width"])
        height = int(self.canvas["height"])
        color = self.GRID_COLOR_DARK if dark_mode else self.GRID_COLOR_LIGHT

        for x in range(0, width, self.GRID_SPACING):
            self.canvas.create_line(x, 0, x, height, fill=color, tags="grid")
        for y in range(0, height, self.GRID_SPACING):
            self.canvas.create_line(0, y, width, y, fill=color, tags="grid")

    def redraw(self, strokes, grid_enabled=False, dark_mode=False):
        """Limpia el lienzo y vuelve a pintar fondo + grid + todos los trazos guardados."""
        self.clear_canvas()
        self.canvas.config(bg=self.BG_DARK if dark_mode else self.BG_LIGHT)

        if grid_enabled:
            self.draw_grid(dark_mode)

        for stroke in strokes:
            for x, y in stroke["points"]:
                self.draw_pixel(x, y, color=stroke["color"], size=stroke.get("thickness", 1))
