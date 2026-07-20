

class DDA:
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.calculate_increments()

    def calculate_increments(self) -> None:
        # Delta X / Y
        self.dx = self.x2 - self.x1
        self.dy = self.y2 - self.y1

        self.steps = max(abs(self.dx), abs(self.dy))
        self.x_increment = self.dx / self.steps if self.steps != 0 else 0
        self.y_increment = self.dy / self.steps if self.steps != 0 else 0

    def set_points(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.calculate_increments()

    def generate_points(self) -> list:
        points = []
        x = self.x1
        y = self.y1

        for _ in range(self.steps + 1):
            points.append((round(x), round(y)))
            x += self.x_increment
            y += self.y_increment

        return points
    
    def print_points(self) -> None:
        points = self.generate_points()
        for point in points:
            print(point)

    def __str__(self) -> str:
        return f"DDA Line from ({self.x1}, {self.y1}) to ({self.x2}, {self.y2}) with {self.steps} steps."
    

class Bresenham:
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def generate_points(self) -> list:
        points = []
        dx = abs(self.x2 - self.x1)
        dy = abs(self.y2 - self.y1)

        sx = 1 if self.x1 < self.x2 else -1
        sy = 1 if self.y1 < self.y2 else -1
        
        err = dx - dy

        while True:
            points.append((self.x1, self.y1))
            if self.x1 == self.x2 and self.y1 == self.y2:
                break
            err2 = err * 2
            if err2 > -dy:
                err -= dy
                self.x1 += sx
            if err2 < dx:
                err += dx
                self.y1 += sy

        return points
    
    def print_points(self) -> None:
        points = self.generate_points()
        for point in points:
            print(point)

    def __str__(self) -> str:
        return f"Bresenham Line from ({self.x1}, {self.y1}) to ({self.x2}, {self.y2})."
    

if __name__ == "__main__":
    dda = DDA(3, 5, 17, 23)
    print(dda)
    dda.print_points()
    print("\nUpdating points...\n")
    dda.set_points(23, 20, 7, 3)
    print(dda)
    dda.print_points()
    print("\nUpdating points...\n")
    dda.set_points(8, 1, 8, 18)
    print(dda)
    dda.print_points()
