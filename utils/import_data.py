import csv

class ImportData:
    def __init__(self, filename):
        self.filename = filename

    def import_from_csv(self):
        """Lee un CSV con el mismo formato que ExportData.export_to_csv y reconstruye
        una lista de trazos ({"tool", "points", "color", "thickness", "groups"}), agrupando
        las filas por `trazo_id` y preservando el orden en que aparecen en el archivo."""
        strokes_by_id = {}
        order = []

        with open(self.filename, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                trazo_id = row.get("trazo_id", "1")
                x, y = int(row["x"]), int(row["y"])

                if trazo_id not in strokes_by_id:
                    strokes_by_id[trazo_id] = {
                        "tool": row.get("herramienta") or "IMPORTADO",
                        "points": [],
                        "color": row.get("color") or "black",
                        "thickness": int(row.get("grosor") or 1),
                        "groups": [],
                    }
                    order.append(trazo_id)

                stroke = strokes_by_id[trazo_id]
                stroke["points"].append((x, y))
                stroke["groups"].append(row.get("grupo") or "N/A")

        return [strokes_by_id[tid] for tid in order]
