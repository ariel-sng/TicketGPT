# Informe Técnico del Proyecto

## 1. Visión General de la Arquitectura

El proyecto consiste en una API REST desarrollada con FastAPI que actúa como asistente virtual para responder consultas de clientes de un e-commerce utilizando modelos de lenguaje de OpenAI.

La solución fue diseñada con una arquitectura modular simple. La estructura principal se compone de los siguientes módulos:

```text
src/
├── main.py: inicializa la aplicación y define el endpoint principal.
├── models: contiene los modelos Pydantic utilizados para validar la estructura de entrada y salida.
│   ├── chat_request.py
│   └── chat_response_ai.py
├── utils
│   ├── openai_service.py: encapsula la lógica de interacción con la API de OpenAI.
│   ├── prompt_loader.py: carga el system prompt desde un archivo externo.
│   └── logger.py: registra métricas de ejecución en formato CSV.
└── test: incluye pruebas unitarias para validar el comportamiento de la integración.
    └── test_openai_service.py

prompt
└── main_prompt.txt: contiene el System Prompt principal del proyecto

metrics
└── metrics.csv: métricas que se guardan por cada llamado a la IA (se crea al momento de hacer el primer llamado)
```

El endpoint recibe una consulta del usuario, la envía al modelo `gpt-4.1-mini` y retorna una respuesta estructurada en formato JSON con los siguientes campos:

- `answer`: respuesta generada por el asistente.
- `confidence`: estimación de confianza entre 0 y 1.
- `recommended_actions`: lista de acciones sugeridas.

## 2. Modelo Seleccionado y Justificación

Se eligió el modelo `gpt-4.1-mini` por ofrecer una buena relación entre costo, velocidad y calidad de respuesta. Como el objetivo del proyecto es responder consultas relativamente acotadas dentro del dominio y no realizar razonamiento complejo, este modelo resulta suficiente para generar respuestas consistentes con un costo muy bajo por invocación.

## 3. Técnicas de Prompting Utilizadas

Se utilizó un **system prompt** almacenado en un archivo externo para definir el comportamiento del modelo como asistente especializado en soporte para e-commerce.

La técnica principal aplicada fue **few-shot prompting**, incorporando ejemplos representativos de preguntas y respuestas dentro del prompt. Esta estrategia permite establecer con mayor claridad el formato esperado y mejorar la consistencia de las respuestas.

Adicionalmente, se configuró una **temperatura de 0.1**, con el objetivo de reducir la variabilidad del modelo y obtener respuestas lo más determinísticas y "simplista" posible. Esto resulta especialmente útil cuando se requiere un comportamiento predecible y estructurado.

## 4. Métricas y Resultados de Muestra

En cada invocación al modelo se registran métricas operativas en un archivo CSV:

- Tokens del prompt (`tokens_prompt`)
- Tokens de la respuesta (`tokens_completions`)
- Tokens totales (`total_tokens`)
- Latencia en milisegundos (`latency_ms`)
- Costo estimado en USD (`estimated_cost_usd`)

### Ejemplo de ejecución

| Métrica | Valor |
|------|------:|
| Tokens del prompt | 100 |
| Tokens de la respuesta | 50 |
| Tokens totales | 150 |
| Latencia | 500 ms |
| Costo estimado | USD 0.000412 |

Estas métricas permiten monitorear el consumo de recursos y estimar el costo operativo de cada consulta.

## 5. Validación y Testing

Se implementó un test unitario para verificar el correcto funcionamiento del servicio que interactúa con OpenAI. Para ello se utilizaron mocks, evitando llamadas reales a la API.

Entre las validaciones realizadas se incluye la comprobación de que el cálculo de tokens y costos sea consistente, es decir, que para una misma respuesta simulada los valores obtenidos sean siempre los esperados.

## 6. Desafíos Encontrados

Los principales desafíos del proyecto estuvieron relacionados con:

- La integración de Structured Outputs con `responses.parse()` en vez de `responses.create()`, para poder pasar el formato de la respuesta directamente con una clase en vez de un JSON schema.
- La implementación de tests unitarios utilizando mocks.
- El cálculo y registro de métricas de uso.

Al ser un proyecto que se centra en el uso de la IA, no se incorporaron mecanismos exhaustivos de manejo de errores, priorizando la claridad y simplicidad del código.

## 7. Posibles Mejoras

En una evolución futura del proyecto completo podrían incorporar las siguientes mejoras:

- Mejor manejo de excepciones para errores de red o validación
- Separación de configuración sensible mediante variables de entorno.
- Aplicación de un patrón de diseño, como Strategy, para abstraer el proveedor de inteligencia artificial y permitir implementar fácilmente distintas soluciones (por ejemplo, OpenAI, Anthropic o modelos locales).
- Automatización de tests en un pipeline de integración continua.
