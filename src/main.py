from fastapi import FastAPI
from dotenv import load_dotenv
from openai import OpenAI

from src.models.chat_request import ChatRequest
from src.utils.prompt_loader import get_system_prompt
from src.utils.openai_service import ask_openai, log_metrics
 
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


@app.get("/system_prompt")
def root():    
    # Simplemente está por motivos didácticos ver el system_prompt, en la vida real no lo expondría
    return { "system_prompt": system_prompt }


@app.post("/chat")
def chatear(request: ChatRequest):
    response, latency = ask_openai(client, system_prompt, request.prompt)
    log_metrics(response, latency)
    result = response.output_parsed.model_dump()
    return result