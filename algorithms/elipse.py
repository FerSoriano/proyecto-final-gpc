import math

class ElipsePM:
    def __init__(self, radius_x: int, radius_y: int, x_center: int, y_center: int):
        self.radius_x = radius_x
        self.radius_y = radius_y
        self.x_center = x_center
        self.y_center = y_center
    
    def generate_initial_points(self) -> list:
        aux_x = 0
        aux_y = self.radius_y
        points = []

        RADIUS_X2 = self.radius_x**2
        RADIUS_Y2 = self.radius_y**2

        # -- Region 1 --
        # P1 inicial
        points.append((aux_x, aux_y))
        p = RADIUS_Y2 - (RADIUS_X2 * self.radius_y) + (RADIUS_X2 / 4)

        aux_radius_y2 = (2 * RADIUS_Y2) * aux_x
        aux_radius_x2 = (2 * RADIUS_X2) * aux_y

        while aux_radius_y2 < aux_radius_x2:
            aux_radius_y2 = (2 * RADIUS_Y2) * aux_x
            aux_radius_x2 = (2 * RADIUS_X2) * aux_y
            aux_x += 1

            if p < 0:
                p = p + aux_radius_y2 + RADIUS_Y2
            else:
                aux_y -= 1
                p = p + aux_radius_y2 + RADIUS_Y2 - aux_radius_x2
            
            points.append((aux_x, aux_y))

        # -- Region 2 --
        # P1 inicial
        p = RADIUS_Y2 * math.pow((aux_x + 1/2), 2) + RADIUS_X2 * math.pow((aux_y - 1), 2) - (RADIUS_X2 * RADIUS_Y2)
        
        while aux_y > 0:
            aux_radius_y2 = (2 * RADIUS_Y2) * aux_x
            aux_radius_x2 = (2 * RADIUS_X2) * aux_y
            aux_y -= 1

            if p > 0:
                p = p - aux_radius_x2 + RADIUS_X2
            else:
                aux_x += 1
                p = p + aux_radius_y2 - aux_radius_x2 + RADIUS_X2

            points.append((aux_x, aux_y))

        return points
    
    def generate_quadrant_points(self) -> dict:
        initial_points = self.generate_initial_points()

        quadrant_points = {f'quadrant_{i}': [] for i in range(1, 5)}

        for x, y in initial_points:
            quadrant_points['quadrant_1'].append((x + self.x_center, y + self.y_center))   
            quadrant_points['quadrant_2'].append((-x + self.x_center, y + self.y_center))  
            quadrant_points['quadrant_3'].append((x + self.x_center, -y + self.y_center))  
            quadrant_points['quadrant_4'].append((-x + self.x_center, -y + self.y_center))

        return quadrant_points
    
    def print_points(self) -> None:
        for quadrant, point_list in self.generate_quadrant_points().items():
            print(f"{quadrant}: {point_list}")

    def __str__(self) -> str:
        return f"Elipse | Coords: ({self.x_center}, {self.y_center}), Radius X: ({self.radius_x}), Radius Y: ({self.radius_y})."
    

if __name__ == "__main__":
    elipse = ElipsePM(
         radius_x=8,
         radius_y=6,
         x_center=15,
         y_center=15

    )
    print(elipse)
    elipse.print_points()