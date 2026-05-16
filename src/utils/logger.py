from datetime import datetime
from pathlib import Path
import json


def log(data: dict, file_name: str = "metrics.jsonl") -> None:
    '''Log simple que recibe un diccionario de Python y lo guarda en un archivo'''
    log_path = Path(__file__).parent.parent.parent / "metrics" / file_name

    # para crear la carpeta si no existe
    log_path.parent.mkdir(exist_ok=True)

    data_with_timestamp = {
        "timestamp": datetime.now().isoformat(),
        **data
    }

    # a falta de BBDD no relacional, se abre un archivo en lectura y se modifica
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data_with_timestamp, ensure_ascii=False) + "\n")