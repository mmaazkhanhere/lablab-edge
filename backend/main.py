import os
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from models.emotion_analyzer import emotion_analyzer
from models.image_generation import image_generation


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

@app.post('/image')
async def image_analyzer(input: UserMemory):
    try:
        image_path = image_generation(input.memory)
        if not os.path.exists(image_path):
            logger.error(f"Image not found at path: {image_path}")
            raise HTTPException(status_code=404, detail="Image not found.")
        
        logger.info(f"Sending image from path: {image_path}")
        return FileResponse(image_path, media_type="image/png", filename="image.png")
    
    except HTTPException as http_exc:
        logger.error(f"HTTPException: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))