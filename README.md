# TicketGPT

API desarrollada con Python, FastAPI y OpenAI.
Práctica de AI Engineering

## Requisitos

- Python 3.10 o superior
- Git

## Estructura del proyecto

```text
TicketGPT/
│── src/
│   └── main.py
│── .vscode/
│   └── launch.json
│── .venv/
│── .env
│── .gitignore
│── requirements.txt
│── README.md
```

## 1. Clonar el repositorio

```bash
git clone https://https://github.com/ariel-sng/TicketGPT.git
cd TicketGPT
```

## 2. Crear entorno virtual

```bash
python -m venv .venv
```

## 3. Activar entorno virtual

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

## 4. Instalar dependencias

```bash
pip install -r requirements.txt
```
*Recordar tener el entorno virtual para instalarse las dependencia a nivel global*

## 5. Crear archivo `.env`

Creá un archivo llamado `.env` en la raíz del proyecto con el siguiente contenido:

```env
OPENAI_API_KEY=tu_api_key_acá_porque_no_pienso_gastar_la_mía
```
⚠︎ **Importante:** *Aún no está implementada la lógica con OpenAI, por lo que este paso puede ser ignorado hasta futuros cambios*

## 6. Ejecutar la aplicación

```bash
uvicorn src.main:app --reload
```

## 7. Abrir en el navegador

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

___

### Debug en Visual Studio Code

Dejo subido el `.vscode/launch.json` por si alguno quiere hacer un debug al código en VSC, presionando `F5`. Esto incluye `--reload`, por lo que se puede modificar el código en ejecución y ver los cambios.

### Dependencias principales

- FastAPI
- Uvicorn
- OpenAI
- python-dotenv