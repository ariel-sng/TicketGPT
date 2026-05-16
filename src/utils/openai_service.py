import json
import time
from openai import OpenAI


# precio aproximado de GPT-4.1-mini (USD por 1 millón de tokens)
# fuente: https://openrouter.ai/openai/gpt-4.1-mini
INPUT_PRICE_PER_MILLION = 0.40
OUTPUT_PRICE_PER_MILLION = 1.60


def ask_openai(client: OpenAI, system_prompt: str, user_prompt: str) -> dict:
    '''
        Envía el prompt del usuario a la API de OpenAI y retorna una respuesta estructurada
        con la respuesta del asistente, el nivel de confianza, acciones recomendadas,
        tokens consumidos y costo estimado en USD.
    '''
    
    start_time = time.perf_counter()

    # por ahora, implemento gpt-4.1-mini

    response = client.responses.create(
        model="gpt-4.1-mini",
        temperature=0.1,
        input=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "chat_response",
                "schema": {
                    # no sabía que podía limitar por el propio JSON cosas de la respuesta
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "answer": {
                            "type": "string"
                        },
                        "confidence": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 1
                        },
                        "recommended_actions": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        }
                    },
                    "required": [
                        "answer",
                        "confidence",
                        "recommended_actions"
                    ]
                }
            }
        }
    )

    latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

    result = json.loads(response.output_text)

    total_tokens, estimated_cost_usd = get_price_and_tokens(response)

    result["tokens_used"] = total_tokens
    result["estimated_cost_usd"] = round(estimated_cost_usd, 8)
    result["latency_ms"] = latency_ms

    return result

def get_price_and_tokens(response):
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens
    total_tokens = response.usage.total_tokens

    estimated_cost_usd = (
        (input_tokens / 1_000_000) * INPUT_PRICE_PER_MILLION +
        (output_tokens / 1_000_000) * OUTPUT_PRICE_PER_MILLION
    )
    
    # PUEDO DEVOLVER DOS VALORES ASÍ SIN MÁS? que raro que es este lenguaje
    return total_tokens,estimated_cost_usd