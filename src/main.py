from fastapi import FastAPI
from openai import OpenAI
from dotenv import load_dotenv
from src.models.chat_request import ChatRequest

# para cargar var. de ambiente, aún nada implementado con OpenAI
load_dotenv()

app = FastAPI()

#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def root():
    return { "mensaje": "API funcionando" }

@app.post("/chat")
async def chat(request: ChatRequest):
    return { "recibido": request }