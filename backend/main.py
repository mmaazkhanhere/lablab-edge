from fastapi import FastAPI
from pydantic import BaseModel

from models.emotion_analyzer import emotion_analyzer

class UserMemory(BaseModel):
    memory: str

app: FastAPI = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post('/memory')
async def memory_analyzer(input: UserMemory):
    response  = emotion_analyzer(input.memory)
    return response