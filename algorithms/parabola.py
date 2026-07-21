class ParabolaPM:
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.rango = abs(x2 - x1)
        self.altura = abs(y2 - y1)

        if self.rango == 0:
            raise ValueError("X Final no puede ser igual a X Inicial.")
        if self.altura == 0:
            raise ValueError("Y Final no puede ser igual a Y Inicial.")

        # Dirección de apertura de la parábola: hacia +x o hacia -x,
        # según en qué lado del vértice quedó el punto final.
        self.dir_x = 1 if x2 >= x1 else -1

        # Escala de la parábola (y² = c * x) derivada de los dos puntos,
        # para que el trazo pase exactamente por (x2, y2).
        self.c = (self.altura ** 2) / self.rango

    def generate_initial_points(self) -> list:
        """Punto medio en 2 regiones para y² = c·x (igual idea que ElipsePM):
        Región 1 (cerca del vértice, pendiente > 1): dominante en Y, decide X.
        Región 2 (más lejos, pendiente <= 1): dominante en X, decide Y.
        Sin las 2 regiones, una parábola con 'c' grande degenera en una recta."""
        aux_x = 0
        aux_y = 0
        points = []

        # Punto inicial (0, 0)
        points.append((aux_x, aux_y))

        # El cambio de región ocurre donde la pendiente (c / 2y) cruza 1, es decir y = c/2
        switch_y = self.c / 2

        # -- Región 1 --
        e = 1 - (self.c / 2)  # F(0.5, 1) = 1² - c*0.5

        while aux_y < self.altura and (aux_y + 1) <= switch_y:
            aux_y += 1
            if e < 0:
                # Siguiente punto: (x_k, y_k+1) -> X se mantiene
                e = e + (2 * aux_y) + 1
            else:
                # Siguiente punto: (x_k+1, y_k+1) -> X también avanza
                aux_x += 1
                e = e + (2 * aux_y) + 1 - self.c

            points.append((aux_x, aux_y))

        # -- Región 2 --
        d = (aux_y + 0.5) ** 2 - self.c * (aux_x + 1)  # F(x+1, y+0.5)

        while aux_x < self.rango:
            aux_x += 1
            if d >= 0:
                # Siguiente punto: (x_k+1, y_k) -> Y se mantiene
                d = d - self.c
            else:
                # Siguiente punto: (x_k+1, y_k+1) -> Y también avanza
                aux_y += 1
                d = d + (2 * aux_y) - self.c

            points.append((aux_x, aux_y))

        return points

    def generate_points(self) -> dict:
        initial_points = self.generate_initial_points()

        symmetry_points = {
            'upper': [],  # (x,  y)
            'lower': [],  # (x, -y)
        }

        for x, y in initial_points:
            real_x = (self.dir_x * x) + self.x1
            symmetry_points['upper'].append((real_x, y + self.y1))
            symmetry_points['lower'].append((real_x, -y + self.y1))

        return symmetry_points

    def print_points(self) -> None:
        for branch, point_list in self.generate_points().items():
            print(f"{branch}: {point_list}")

    def __str__(self) -> str:
        return (f"Parábola PM | Inicial: ({self.x1}, {self.y1}), "
                f"Final: ({self.x2}, {self.y2}).")


if __name__ == "__main__":
    p = ParabolaPM(x1=0, y1=0, x2=10, y2=10)
    print(p)
    p.print_points()
