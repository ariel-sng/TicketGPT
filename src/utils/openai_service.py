import json
import time

from openai import OpenAI
from src.models.chat_response_ai import ChatResponse
from src.utils.logger import log
from src.utils.latency_decorator import measure_latency

# precio aproximado de GPT-4.1-mini (USD por 1 millón de tokens)
# fuente: https://openrouter.ai/openai/gpt-4.1-mini
INPUT_PRICE_PER_MILLION = 0.40
OUTPUT_PRICE_PER_MILLION = 1.60

@measure_latency
def ask_openai(client: OpenAI, system_prompt: str, user_prompt: str) -> dict:
    '''
        Envía el prompt del usuario a la API de OpenAI y retorna una respuesta estructurada
        con la respuesta del asistente, el nivel de confianza, acciones recomendadas,
        tokens consumidos y costo estimado en USD.
    '''
    
    start_time = time.perf_counter()

    # por ahora, implemento gpt-4.1-mini

    response = client.responses.parse(
        model="gpt-4.1-mini",
        temperature=0.1,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        text_format=ChatResponse
    )

    latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
    response.usage.latency_ms = latency_ms
    return response

def log_metrics(response_AI, latency_ms):
    '''
        Recibe una respuesta de OpenAI y registra los tokens, latencia y estimación del costo
    '''
    
    estimated_cost_usd = get_price(response_AI)
    
    register = {}
    register["tokens_prompt"] = response_AI.usage.input_tokens
    register["tokens_completions"] = response_AI.usage.output_tokens
    register["total_tokens"] = response_AI.usage.total_tokens
    register["latency_ms"] = latency_ms
    register["estimated_cost_usd"] = round(estimated_cost_usd, 8)
    log(register)

def get_price(response):
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens

    estimated_cost_usd = (
        (input_tokens / 1_000_000) * INPUT_PRICE_PER_MILLION +
        (output_tokens / 1_000_000) * OUTPUT_PRICE_PER_MILLION
    )
    
    # PUEDO DEVOLVER DOS VALORES ASÍ SIN MÁS? que raro que es este lenguaje
    return estimated_cost_usd