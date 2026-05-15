from pydantic import BaseModel, ConfigDict

# odio con toda mi alma que no haya corchetes y solo se separe por identación, lo que bueno es que me obligó a modularizar en otro archivo
class ChatRequest(BaseModel):
    '''Formato del request que se pegar a mi app'''
    prompt: str

    # si incluye algo más que no sea el prompt, se rechaza el request 
    model_config = ConfigDict(extra="forbid")