from datetime import datetime
from pathlib import Path
import csv

def log(data: dict, file_name: str = "metrics.csv") -> None:
    '''Recibe un diccionario de Python y lo guarda en un archivo formateado como JSON'''
    log_path = Path(__file__).parent.parent.parent / "metrics" / file_name

    # para crear la carpeta si no existe
    log_path.parent.mkdir(exist_ok=True)

    row = {
        "timestamp": datetime.now().isoformat(),
        **data
    }

    file_exists = log_path.exists()

    # a falta de BBDD no relacional, se abre un archivo en lectura y se modifica
    with open(log_path, "a", newline="", encoding="utf-8") as cvs_file:
        writer = csv.DictWriter(cvs_file, fieldnames=row.keys())

        # si no existe el archivo, crea el encabezado
        if not file_exists:
            writer.writeheader()

        writer.writerow(row)
    
    for key, value in row.items():
        print(f"{key:20} |  {value}") 