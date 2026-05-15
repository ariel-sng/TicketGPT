from fastapi import FastAPI
from dotenv import load_dotenv
from openai import OpenAI

from src.models.chat_request import ChatRequest
from src.utils.prompt_loader import get_system_prompt
import os


###     Inicializaciones    ###

load_dotenv()
app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
system_prompt = get_system_prompt()


###         RestAPI         ###

@app.get("/")
def root():
    return { "mensaje": "API funcionando" }

@app.get("/systemprompt")
def root():
    return { "system_prompt": system_prompt }

@app.post("/chat")
def chat(request: ChatRequest):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=request.prompt
    )

    # por ahora que devuelva la respuesta completa del openAI completo
    return {
        "respuesta": response
    }

