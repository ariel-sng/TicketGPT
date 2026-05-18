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
└── README.md
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

## 5. Crear archivo `.env`

Creá un archivo llamado `.env` en la raíz del proyecto con el siguiente contenido:

```env
OPENAI_API_KEY=tu_api_key_acá_porque_no_pienso_gastar_la_mía
```

## 6. Ejecutar la aplicación

```bash
uvicorn src.main:app --reload
```

## 7. Abrir en el navegador

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

## 8. Cómo Probar la API

Una vez iniciada la aplicación, es posible interactuar con el asistente de dos maneras sencillas.

### Opción 1: Interfaz automática de Swagger

FastAPI genera automáticamente una interfaz web interactiva accesible desde:

`http://127.0.0.1:8000/docs`

Desde esta página se puede:

1. Seleccionar el endpoint `POST /chat`.
2. Presionar **Try it out**.
3. Ingresar un JSON con la consulta del usuario.
4. Ejecutar la solicitud y visualizar la respuesta.

Ejemplo de request:

```json
{
  "prompt": "¿Dónde está mi pedido?"
}
```

### Opción 2: Usando Postman

También es posible realizar la solicitud mediante Postman.

- **Método HTTP:** `POST`
- **URL:** `http://127.0.0.1:8000/chat`
- **Content-Type:** `application/json`

En la pestaña **Body**, seleccionar la opción **raw** y el formato **JSON**, e ingresar el siguiente contenido:

```json
{
  "prompt": "¿Dónde está mi pedido?"
}
```

Luego, presionar **Send** para enviar la solicitud.

La API, indistinto del método del método en el que interactuaste, responderá con un objeto JSON estructurado con los siguientes campos:

- `answer`: respuesta generada por el asistente.
- `confidence`: nivel estimado de confianza entre 0 y 1.
- `recommended_actions`: acciones sugeridas en función de la consulta.
  
___

### Debug en Visual Studio Code

Dejo subido el `.vscode/launch.json` por si alguno quiere hacer un debug al código en VSC, presionando `F5`. Esto incluye `--reload`, por lo que se puede modificar el código en ejecución y ver los cambios.

### Dependencias principales

- FastAPI
- Uvicorn
- OpenAI
- python-dotenv

### Test

Para ejecutar los test unitarios, ejecute el siguiente comando:
```bash
python -m unittest src.test.test
```