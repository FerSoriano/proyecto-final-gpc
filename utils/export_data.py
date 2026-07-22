import csv

class ExportData:
    def __init__(self, data):
        self.data = data
        self.filename = "data.csv"

    def set_filename(self, filename):
        self.filename = filename

    def export_to_csv(self, columns: list):
        """Escribe una fila por punto de cada trazo en `self.data`
        (lista de dicts {"tool", "points", "color", "thickness", "groups"}),
        usando solo las columnas pedidas en `columns`. `groups` es una lista
        paralela a `points` con la etiqueta de grupo de cada punto
        (ej. "Octante 3", "Cuadrante 1", "Rama 2", o "N/A" si no aplica)."""
        field_getters = {
            "trazo_id": lambda i, stroke, x, y, group: i,
            "herramienta": lambda i, stroke, x, y, group: stroke["tool"],
            "x": lambda i, stroke, x, y, group: x,
            "y": lambda i, stroke, x, y, group: y,
            "color": lambda i, stroke, x, y, group: stroke["color"],
            "grosor": lambda i, stroke, x, y, group: stroke["thickness"],
            "grupo": lambda i, stroke, x, y, group: group,
        }

        with open(self.filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(columns)

            for i, stroke in enumerate(self.data, start=1):
                groups = stroke.get("groups") or ["N/A"] * len(stroke["points"])
                for (x, y), group in zip(stroke["points"], groups):
                    writer.writerow([field_getters[col](i, stroke, x, y, group) for col in columns])
