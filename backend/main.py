import os
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
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

app.mount("/images", StaticFiles(directory="generated_images"), name="images")

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
        image_response = image_generation(input.memory, num_images=5)
        if not image_response.get("image_urls"):
            logger.error("No images were generated.")
            raise HTTPException(status_code=500, detail="No images were generated.")

        logger.info(f"Generated image URLs: {image_response['image_urls']}")
        return {"image_urls": image_response["image_urls"]}

    except HTTPException as http_exc:
        logger.error(f"HTTPException: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))