
import math

class Circle:
    def __init__(self, x: int, y: int, r: int):
        self.x = x
        self.y = y
        self.r = r

    def generate_initial_points(self) -> list:
        raise NotImplementedError("This method should be implemented by subclasses.")

    def generate_octant_points(self) -> dict:
        initial_points = self.generate_initial_points()

        octant_points = {f'octant_{i}': [] for i in range(1, 9)}

        for x, y in initial_points:
            octant_points['octant_1'].append((x + self.x, y + self.y))   # 1er Octante
            octant_points['octant_2'].append((y + self.x, x + self.y))   # 2do Octante
            octant_points['octant_3'].append((-y + self.x, x + self.y))  # 3er Octante
            octant_points['octant_4'].append((-x + self.x, y + self.y))  # 4to Octante
            octant_points['octant_5'].append((-x + self.x, -y + self.y)) # 5to Octante
            octant_points['octant_6'].append((-y + self.x, -x + self.y)) # 6to Octante
            octant_points['octant_7'].append((x + self.x, -y + self.y))  # 7mo Octante
            octant_points['octant_8'].append((y + self.x, -x + self.y))  # 8vo Octante

        return octant_points

    def print_points(self) -> None:
        for octant, point_list in self.generate_octant_points().items():
            print(f"{octant}: {point_list}")

    def __str__(self) -> str:
        return f"Circle | Coords: ({self.x}, {self.y}), Ratio: ({self.r})."


class DDA(Circle):
    def __init__(self, x: int, y: int, r: int):
        super().__init__(x, y, r)

    def generate_initial_points(self) -> list:
        aux_x = 0
        aux_y = self.r
        points = []

        while aux_x <= aux_y:
            aux_y = round(math.sqrt(self.r**2 - aux_x**2))
            points.append((aux_x, aux_y))
            aux_x += 1

        return points

    def __str__(self) -> str:
        return f"Circle DDA | Coords: ({self.x}, {self.y}), Ratio: ({self.r})."
    

class PuntoMedio(Circle):
    def __init__(self, x: int, y: int, r: int):
        super().__init__(x, y, r)

    def generate_initial_points(self) -> list:
        aux_x = 0
        aux_y = self.r
        points = []

        # Punto inicial
        points.append((aux_x, aux_y))

        # P inicial
        p = 1 - self.r

        while aux_x < aux_y:
            aux_x += 1
            if p < 0:
                p += 2 * aux_x + 1
            else:
                aux_y -= 1
                p += 2 * (aux_x - aux_y) + 1
            
            points.append((aux_x, aux_y))

        return points

    def __str__(self) -> str:
        return f"Circle PM | Coords: ({self.x}, {self.y}), Ratio: ({self.r})."
    

if __name__ == "__main__":
    dda = DDA(
         r=20, x=30, y=25
    )
    print(dda)
    dda.print_points()

    print("\n" + "-"*50 + "\n")

    pm = PuntoMedio(
        r=17, x=24, y=15
    )
    print(pm)
    pm.print_points()
    