from pydantic import BaseModel, Field

class ChatResponse(BaseModel):
    '''Formato a seguir para la respuesta de la IA'''
    answer: str
    confidence: float = Field(ge=0.0, le=1.0)
    recommended_actions: list[str]
