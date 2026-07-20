import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from ui.canvas_manager import CanvasManager

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Proyecto Graficación - Paint")
        self.geometry("1400x650")
        self.resizable(False, False)

        self._create_layout()

    def _create_layout(self):
        # ==========================================
        # MENÚ SUPERIOR: Selección de Color
        # ==========================================
        top_frame = ttk.Frame(self, padding="5")
        top_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(top_frame, text="Color de trazo:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(5, 10))

        # self.colores = ["black", "blue", "pink", "green", "purple"]
        self.colores = {
            "negro": "black", 
            "azul": "blue", 
            "rosa": "pink", 
            "verde": "green", 
            "morado": "purple"
        }
        
        # Diccionario para guardar los cuadritos de color y conectarlos luego en el controlador
        self.color_squares = {} 

        for color_name, color_value in self.colores.items():
            # Usamos un tk.Label simulando un botón para garantizar que el color se pinte correctamente
            square = tk.Label(top_frame, bg=color_value, width=4, height=1, relief="ridge", borderwidth=2, cursor="hand2")
            square.pack(side=tk.LEFT, padx=4)
            self.color_squares[color_name] = square

        # Una línea separadora entre el menú superior y el resto de la interfaz
        ttk.Separator(self, orient='horizontal').pack(fill=tk.X, pady=(0, 5))

        # ==========================================
        # PANEL IZQUIERDO: Herramientas (Botones)
        # ==========================================
        tools_frame = ttk.Frame(self, padding="10")
        tools_frame.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(tools_frame, text="Primitivas", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        self.btn_dda = ttk.Button(tools_frame, text="Línea DDA")
        self.btn_dda.pack(fill=tk.X, pady=2)
        
        self.btn_bresenham = ttk.Button(tools_frame, text="Línea Bresenham")
        self.btn_bresenham.pack(fill=tk.X, pady=2)

        ttk.Separator(tools_frame, orient='horizontal').pack(fill=tk.X, pady=15)

        self.btn_clear = ttk.Button(tools_frame, text="Limpiar Pantalla")
        self.btn_clear.pack(fill=tk.X, pady=2)

        # ==========================================
        # PANEL CENTRAL: Lienzo de Dibujo
        # ==========================================
        canvas_frame = ttk.Frame(self, padding="10")
        canvas_frame.pack(side=tk.LEFT, expand=True)
        
        self.canvas_manager = CanvasManager(canvas_frame)
        self.canvas_manager.get_widget().pack()

        # ==========================================
        # PANEL DERECHO: Registro de Cálculos
        # ==========================================
        log_frame = ttk.Frame(self, padding="10")
        log_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        ttk.Label(log_frame, text="Cálculos de Coordenadas", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, width=45, height=35, state='disabled')
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def log_calculation(self, text):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        
    def clear_log(self):
        self.log_text.config(state='normal')
        self.log_text.delete('1.0', tk.END)
        self.log_text.config(state='disabled')