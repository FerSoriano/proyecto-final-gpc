import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from ui.canvas_manager import CanvasManager

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Proyecto Graficación - Paint")
        self.geometry("1450x650")
        self.resizable(False, False)

        self._create_layout()

    def _create_layout(self):
        # ==========================================
        # MENÚ SUPERIOR: Selección de Color
        # ==========================================
        top_frame = ttk.Frame(self, padding="5")
        top_frame.pack(side=tk.TOP, fill=tk.X)

        # Panel para seleccionar el modo de entrada
        mode_frame = ttk.Frame(top_frame)
        mode_frame.pack(side=tk.LEFT, padx=(0, 20))

        ttk.Label(mode_frame, text="Entrada:", font=("Arial", 15, "bold")).pack(side=tk.LEFT, padx=(5, 5))

        self.btn_coords = ttk.Button(mode_frame, text="Coordenadas")
        self.btn_coords.pack(side=tk.LEFT, padx=2)

        # Alineado al lado derecho de la barra superior
        self.btn_export = ttk.Button(top_frame, text="Exportar CSV")
        self.btn_export.pack(side=tk.RIGHT, padx=(2, 5))

        # Separador visual vertical
        ttk.Separator(top_frame, orient='vertical').pack(side=tk.LEFT, fill=tk.Y, padx=10)

        # Panel para seleccionar el color de trazo
        ttk.Label(top_frame, text="Color de trazo:", font=("Arial", 15, "bold")).pack(side=tk.LEFT, padx=(5, 10))

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

        # Separador visual vertical
        ttk.Separator(top_frame, orient='vertical').pack(side=tk.LEFT, fill=tk.Y, padx=10)

        # Panel para seleccionar el grosor de trazo
        ttk.Label(top_frame, text="Grosor:", font=("Arial", 15, "bold")).pack(side=tk.LEFT, padx=(5, 5))

        self.thickness_var = tk.IntVar(value=1)
        self.spinbox_thickness = ttk.Spinbox(top_frame, from_=1, to=10, textvariable=self.thickness_var, width=4)
        self.spinbox_thickness.pack(side=tk.LEFT, padx=(0, 10))

        # Una línea separadora entre el menú superior y el resto de la interfaz
        ttk.Separator(self, orient='horizontal').pack(fill=tk.X, pady=(0, 5))

        # ==========================================
        # PANEL IZQUIERDO: Herramientas (Botones)
        # ==========================================
        tools_frame = ttk.Frame(self, padding="10")
        tools_frame.pack(side=tk.LEFT, fill=tk.Y)

        # -- Lineas --
        ttk.Label(tools_frame, text="Lineas", font=("Arial", 20, "bold")).pack(pady=(0, 10))
        
        self.btn_dda = ttk.Button(tools_frame, text="Línea DDA", width=16)
        self.btn_dda.pack(fill=tk.X, pady=2)
        
        self.btn_bresenham = ttk.Button(tools_frame, text="Línea Bresenham", width=16)
        self.btn_bresenham.pack(fill=tk.X, pady=2)
        
        # -- Circulos --
        ttk.Separator(tools_frame, orient='horizontal').pack(fill=tk.X, pady=15)

        ttk.Label(tools_frame, text="Círculos", font=("Arial", 20, "bold")).pack(pady=(0, 10))

        self.btn_dda_circle = ttk.Button(tools_frame, text="Círculo DDA", width=16)
        self.btn_dda_circle.pack(fill=tk.X, pady=2)
        self.btn_pm_circle = ttk.Button(tools_frame, text="Círculo PM", width=16)
        self.btn_pm_circle.pack(fill=tk.X, pady=2)

        # -- Elipse --
        ttk.Separator(tools_frame, orient='horizontal').pack(fill=tk.X, pady=15)
        ttk.Label(tools_frame, text="Elipses", font=("Arial", 20, "bold")).pack(pady=(0, 10))
        self.btn_pm_ellipse = ttk.Button(tools_frame, text="Elipse PM", width=16)
        self.btn_pm_ellipse.pack(fill=tk.X, pady=2)

        # -- Parábola --
        ttk.Separator(tools_frame, orient='horizontal').pack(fill=tk.X, pady=15)
        ttk.Label(tools_frame, text="Parábolas", font=("Arial", 20, "bold")).pack(pady=(0, 10))
        self.btn_pm_parabola = ttk.Button(tools_frame, text="Parábola PM", width=16)
        self.btn_pm_parabola.pack(fill=tk.X, pady=2)


        # ==========================================
        # Botones de acción: Limpiar y Salir
        # ==========================================
        ttk.Separator(tools_frame, orient='horizontal').pack(fill=tk.X, pady=15)

        # Botón estilo Bootstrap Primary (Azul) para Limpiar
        self.btn_clear = tk.Label(tools_frame, text="Limpiar Pantalla", bg="#0d6efd", fg="white", 
                                  font=("Arial", 13, "bold"), pady=8, cursor="hand2")
        self.btn_clear.pack(fill=tk.X, pady=2)

        # Botón estilo Bootstrap Danger (Rojo) para Salir
        self.btn_exit = tk.Label(tools_frame, text="Salir", bg="#dc3545", fg="white", 
                                 font=("Arial", 13, "bold"), pady=8, cursor="hand2")
        self.btn_exit.pack(fill=tk.X, pady=(20, 2))
        

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
        
        # Sub-contenedor para alinear el título y el botón de opciones
        log_header = ttk.Frame(log_frame)
        log_header.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(log_header, text="Cálculos de Coordenadas", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        
        self.btn_options = ttk.Button(log_header, text="⚙️ Opciones")
        self.btn_options.pack(side=tk.RIGHT)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, width=45, height=35, state='disabled', font=("Arial", 12))
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