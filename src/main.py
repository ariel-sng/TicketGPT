from fastapi import FastAPI
from openai import OpenAI

from dotenv import load_dotenv
import os

from src.models.chat_request import ChatRequest
from pathlib import Path

# para cargar var. de ambiente, aún nada implementado con OpenAI
load_dotenv()
app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def root():
    return { "mensaje": "API funcionando" }

@app.post("/chat")
async def chat(request: ChatRequest):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=request.prompt
    )

    # por ahora que devuelva la respuesta completa del openAI completo
    return {
        "respuesta": response
    }

@app.get("/systemprompt")
def root():
    main_prompt = getSystemPrompt()

    return { "system_prompt": main_prompt }

def getSystemPrompt():
    PROMPT_PATH = Path(__file__).parent.parent / "prompt" / "main_prompt.txt"

    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        main_prompt = f.read()
    return main_prompt