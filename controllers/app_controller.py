import tkinter as tk
from tkinter import ttk, messagebox
from algorithms.lineas import DDA, Bresenham
from algorithms.circunferencias import DDA as DDA_Circle, PuntoMedio
from algorithms.elipse import ElipsePM

class AppController:
    def __init__(self, view):
        self.view = view
        self.canvas_manager = self.view.canvas_manager
        
        # Estado de la aplicación
        self.current_mode = None  
        self.start_x = None
        self.start_y = None
        self.current_color = self.view.colores["negro"]  # Color por defecto
        self.input_mode = "Mouse"  # Modo de entrada por defecto
        self.log_font_size = 12  # Tamaño inicial por defecto
        
        # Conectar botón de opciones
        self.view.btn_options.config(command=self.open_options_popup)

        style = ttk.Style()
        style.configure("Default.TButton", font=("Arial", 15), foreground="white")
        style.configure("Active.TButton", font=("Arial", 15, "bold"), foreground="white") # Azul Bootstrap

        # Agrupar los botones usando las mismas llaves que tus strings de modo
        self.tool_buttons = {
            "LINEA DDA": self.view.btn_dda,
            "LINEA BRESENHAM": self.view.btn_bresenham,
            "CIRCULO DDA": self.view.btn_dda_circle,
            "CIRCULO PM": self.view.btn_pm_circle,
            "ELIPSE PM": self.view.btn_pm_ellipse
        }

        # Aplicar el estilo por defecto a todos al iniciar
        for btn in self.tool_buttons.values():
            btn.config(style="Default.TButton")
        # ----------------------------------------

        # 1. Conectar botones de herramientas
        self.view.btn_dda.config(command=lambda: self.set_mode("LINEA DDA"))
        self.view.btn_bresenham.config(command=lambda: self.set_mode("LINEA BRESENHAM"))
        self.view.btn_dda_circle.config(command=lambda: self.set_mode("CIRCULO DDA"))
        self.view.btn_pm_circle.config(command=lambda: self.set_mode("CIRCULO PM"))
        self.view.btn_pm_ellipse.config(command=lambda: self.set_mode("ELIPSE PM"))

        self.view.btn_clear.bind("<Button-1>", lambda event: self.clear_canvas())
        self.view.btn_exit.bind("<Button-1>", lambda event: self.confirm_exit())

        self.view.btn_coords.config(command=self.open_coordinates_popup)

        # 2. Conectar la selección de colores del menú superior
        for color_name, square_widget in self.view.color_squares.items():
            # c=color_name asegura que se pase el color correcto en la función lambda
            square_widget.bind("<Button-1>", lambda event, c=color_name: self.set_color(c))

        # 3. Conectar el lienzo
        self.canvas_manager.canvas.bind("<Button-1>", self.on_canvas_click)



    def set_input_mode(self, mode):
        self.input_mode = mode
        self.view.log_calculation(f"👨🏽‍💻 Modo de entrada: {mode.upper()}")

    def open_coordinates_popup(self):
        """Abre un pop-up modal para ingresar coordenadas manuales."""
        self.set_input_mode("coordenadas")

        if not self.current_mode:
            self.view.log_calculation("\nℹ️ Selecciona primero una primitiva para ingresar coordenadas.\n")
            return

        # Construir ventana modal
        popup = tk.Toplevel(self.view)
        popup.title(f"Coordenadas - {self.current_mode}")
        popup.geometry("300x250")
        popup.resizable(False, False)
        popup.transient(self.view)  # Se ata a la ventana principal
        popup.grab_set()  # Bloquea la ventana principal hasta que se cierre el pop-up

        # Preparar los campos según la primitiva seleccionada
        if self.current_mode in ["LINEA DDA", "LINEA BRESENHAM"]:
            campos = ["X Inicial", "Y Inicial", "X Final", "Y Final"]
        elif self.current_mode in ["CIRCULO DDA", "CIRCULO PM"]:
            campos = ["Radio", "X Central", "Y Central"]
        elif self.current_mode in ["ELIPSE PM"]:
            campos = ["Radio X", "Radio Y", "X Central", "Y Central"]

        entradas = {}
        for campo in campos:
            frame = ttk.Frame(popup, padding=5)
            frame.pack(fill=tk.X)
            ttk.Label(frame, text=f"{campo}:", width=10).pack(side=tk.LEFT)
            entry = ttk.Entry(frame)
            entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
            entradas[campo] = entry

        def procesar_formulario():
            try:
                # Extraer y convertir a enteros
                valores = {campo: int(entry.get()) for campo, entry in entradas.items()}
                popup.destroy()
                
                # Por ahora, como solo hay líneas, mapeamos directamente
                if self.current_mode in ["LINEA DDA", "LINEA BRESENHAM"]:
                    self.draw_lines(
                        valores["X Inicial"], 
                        valores["Y Inicial"], 
                        valores["X Final"], 
                        valores["Y Final"]
                    )
                elif self.current_mode in ["CIRCULO DDA", "CIRCULO PM"]:
                    self.draw_circle(
                        radius = valores["Radio"],
                        x_center = valores["X Central"],   
                        y_center = valores["Y Central"]
                    )
                elif self.current_mode in ["ELIPSE PM"]:
                    self.draw_ellipse(
                        radius_x = valores["Radio X"],
                        radius_y = valores["Radio Y"],
                        x_center = valores["X Central"],   
                        y_center = valores["Y Central"]
                    )

            except ValueError:
                self.view.log_calculation("❌ ERROR: Por favor, ingresa únicamente números enteros.")


        ttk.Button(popup, text="Dibujar", command=procesar_formulario).pack(pady=15)

    def open_options_popup(self):
        """Abre un pop-up modal para configurar opciones generales de la interfaz."""
        popup = tk.Toplevel(self.view)
        popup.title("Opciones del Registro")
        popup.geometry("280x150")
        popup.resizable(False, False)
        popup.transient(self.view)
        popup.grab_set()

        # Contenedor para el tamaño de letra
        frame = ttk.Frame(popup, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Tamaño de letra (Logs):", font=("Arial", 12)).pack(side=tk.LEFT, padx=(0, 10))

        # Spinbox atado a una variable de control de Tkinter
        size_var = tk.IntVar(value=self.log_font_size)
        spinbox = ttk.Spinbox(frame, from_=8, to_=24, textvariable=size_var, width=5)
        spinbox.pack(side=tk.LEFT)

        def apply_changes():
            # Actualizamos la variable global
            self.log_font_size = size_var.get()
            
            # Cambiamos dinámicamente la fuente del log principal
            self.view.log_text.config(font=("Arial", self.log_font_size))
            
            self.view.log_calculation(f"⚙️ Tamaño de letra actualizado a: {self.log_font_size}")
            popup.destroy()

        ttk.Button(popup, text="Aplicar y Cerrar", command=apply_changes).pack(side=tk.BOTTOM, pady=(10, 0))


    def set_color(self, color):
        """Actualiza el color activo para los siguientes trazos."""
        self.current_color = self.view.colores[color]
        self.view.log_calculation(f"🎨 Color cambiado a: {color.capitalize()}")

    def set_mode(self, mode):
        self.current_mode = mode
        self.view.log_calculation(f"ℹ️ Modo seleccionado: {mode}")
        self.start_x = None
        self.start_y = None

        # Restaurar todos los botones a su estilo por defecto
        for btn in self.tool_buttons.values():
            btn.config(style="Default.TButton")
            
        # Resaltar solo el botón que acaba de ser seleccionado
        if mode in self.tool_buttons:
            self.tool_buttons[mode].config(style="Active.TButton")

    def clear_canvas(self):
        self.canvas_manager.clear_canvas()
        self.view.clear_log()
        self.view.log_calculation("🧹 Pantalla y registro limpios")
        self.start_x = None
        self.start_y = None

    def on_canvas_click(self, event):
        if not self.current_mode:
            self.view.log_calculation("ℹ️ Selecciona primero una primitiva para dibujar.")
            return
        
        if self.current_mode in ["CIRCULO DDA", "CIRCULO PM", "ELIPSE PM"]:
            self.view.log_calculation(f"\n⚠️ Utiliza el botón 'Coordenadas'\n")
            return

        if self.start_x is None and self.start_y is None:
            self.start_x = event.x
            self.start_y = event.y
            self.view.log_calculation(f"Punto inicial (x1, y1): ({self.start_x}, {self.start_y})")
        else:
            end_x = event.x
            end_y = event.y
            self.view.log_calculation(f"Punto final (x2, y2): ({end_x}, {end_y})")
            
            self.draw_lines(self.start_x, self.start_y, end_x, end_y)
            
            self.start_x = None
            self.start_y = None

    def draw_lines(self, x1, y1, x2, y2):
        points = []
        
        if self.current_mode == "LINEA DDA":
            alg = DDA(x1, y1, x2, y2)
            points = alg.generate_points()
        elif self.current_mode == "LINEA BRESENHAM":
            alg = Bresenham(x1, y1, x2, y2)
            points = alg.generate_points()

        self.view.log_calculation(f"\n⌛️ Calculando {self.current_mode}...\n")
        
        for p in points:
            # Ahora le pasamos el color actual al método que pinta el pixel
            self.canvas_manager.draw_pixel(p[0], p[1], color=self.current_color)
            self.view.log_calculation(f"X: {p[0]}, Y: {p[1]}")
        
        self.view.log_calculation("\n✅ Trazo finalizado\n")

    def draw_circle(self, x_center, y_center, radius):
        points_dict = {}

        if self.current_mode == "CIRCULO DDA":
            dda_circle = DDA_Circle(
                x=x_center, y=y_center, r=radius
            )
            points_dict = dda_circle.generate_octant_points()
            dda_circle.print_points()

        elif self.current_mode == "CIRCULO PM":
            pm_circle = PuntoMedio(
                x=x_center, y=y_center, r=radius
            )
            points_dict = pm_circle.generate_octant_points()
            pm_circle.print_points()

        else:
            self.view.log_calculation("⚠️ Primitiva no reconocida para dibujar círculos.")
            return

        self._draw_circle_and_ellipse_detail("circle", points_dict)

    def draw_ellipse(self, radius_x: int, radius_y: int, x_center: int, y_center: int):
        pm_elipse = ElipsePM(
            radius_x=radius_x,
            radius_y=radius_y,
            x_center=x_center,
            y_center=y_center
        )
        points_dict = pm_elipse.generate_quadrant_points()
        pm_elipse.print_points()

        self._draw_circle_and_ellipse_detail("ellipse", points_dict)

    
    def _draw_circle_and_ellipse_detail(self, primitive_name: str, points_dict: dict) -> None:

        quadrants_octants = "octantes" if primitive_name == "circle" else "cuadrantes"

        self.view.log_calculation(f"\n⌛️ Calculando {self.current_mode}...")

        for _, points in points_dict.items():
            for p in points:
                self.canvas_manager.draw_pixel(p[0], p[1], color=self.current_color)

        self.view.log_calculation("\n✅ Trazo finalizado\n")

        # Crear e inyectar el botón dinámico en la caja de texto
        self.view.log_text.config(state='normal')
        
        btn_detalle = ttk.Button(self.view.log_text, text=f"Mostrar detalle de {quadrants_octants}", 
                                    command=lambda: self.show_points_details(primitive_name ,points_dict))
        
        # Insertar el widget dentro del log
        self.view.log_text.window_create(tk.END, window=btn_detalle)
        self.view.log_text.insert(tk.END, "\n\n")
        
        self.view.log_text.see(tk.END)
        self.view.log_text.config(state='disabled')
        

    def confirm_exit(self, event=None):
        """Muestra un diálogo de confirmación antes de cerrar la aplicación."""
        respuesta = messagebox.askyesno("Confirmar Salida", "¿Estás seguro de que deseas salir del programa?")
        if respuesta:
            self.view.destroy()

    def show_points_details(self, primitive_name: str, points_dict: dict) -> None:
        """Abre una ventana independiente con el desglose de los cuadrantes / octantes."""
        detalle_win = tk.Toplevel(self.view)
        title = "Círculo" if primitive_name == "circle" else "Elipse"
        detalle_win.title(f"Detalle de Coordenadas - {title}")
        detalle_win.geometry("350x500")
        detalle_win.resizable(False, False)

        from tkinter import scrolledtext
        txt_detalles = scrolledtext.ScrolledText(detalle_win, width=40, height=25, font=("Arial", self.log_font_size))
        txt_detalles.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Poblar la ventana con los datos del diccionario
        headers = "OCTANTE" if primitive_name == "circle" else "CUADRANTE"
        for x, points in enumerate(points_dict.values(), start=1):
            txt_detalles.insert(tk.END, f"--- {headers}: {x} ---\n")
            for p in points:
                txt_detalles.insert(tk.END, f"X: {p[0]}, Y: {p[1]}\n")
            txt_detalles.insert(tk.END, "\n")

        # Bloquear escritura
        txt_detalles.config(state='disabled')