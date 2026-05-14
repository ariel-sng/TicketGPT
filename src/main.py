from fastapi import FastAPI
from openai import OpenAI
from dotenv import load_dotenv
import os

# para cargar var. de ambiente, aún nada implementado con OpenAI
load_dotenv()

app = FastAPI()

#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def root():
    return {"mensaje": "API funcionando"}
