from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from models.emotion_analyzer import emotion_analyzer

class UserMemory(BaseModel):
    memory: str

app: FastAPI = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post('/memory')
async def memory_analyzer(input: UserMemory):
    response  = emotion_analyzer(input.memory)
    return response