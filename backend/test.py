from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from models.updated_prompt_image_generation import prompt_for_images
from models.prompt_for_music_generation import prompt_for_music
from models.music_generation import generate_music
from models.emotion_therapy import emotion_therapy

# from models.emotion_therapy_aria import emotion_therapy_aria

import requests
import os

ALLEGRO_API_KEY = os.getenv('ALLEGRO_API_KEY')

class UserMemory(BaseModel):
    memory: str

class EmotionallyTherapyResponse(BaseModel):
    ai_response: str

class MusicResponse(BaseModel):
    audio_url: str

app: FastAPI = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

current_dir = os.path.dirname(__file__)
images_dir = os.path.join(current_dir, "generated_images")
music_dir = os.path.join(current_dir, "generated_music")

app.mount("/images", StaticFiles(directory=images_dir), name="images")
app.mount("/music", StaticFiles(directory=music_dir), name="music")
# import logging
# logging.basicConfig(level=logging.INFO)
@app.get("/")
async def root():
    # logging.info("Root endpoint accessed.")
    return {"message": "Revisit Therapy App"}

# Emotional therapy API endpoint
@app.post('/emotion-therapy')
async def memory_emotional_therapy(input: UserMemory):
    # logging.info("Emotion therapy endpoint called.")
    response = emotion_therapy(input.memory)
    return response

# Image generation endpoint
@app.post('/image')
async def image_analyzer(input: UserMemory):
    try:
        prompt: str = prompt_for_images(input.memory)
        image_response = image_generation(prompt, num_images=4)
        if not image_response.get("image_urls"):
            raise HTTPException(status_code=500, detail="No images were generated.")

        return {"image_urls": image_response["image_urls"]}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Music generation endpoint
@app.post('/music')
async def music_generator(input: UserMemory):
    try:
        prompt = prompt_for_music(input.memory)
        audio_url = generate_music(prompt)
        return MusicResponse(audio_url=audio_url)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

# Video generation endpoint
@app.post('/video')
async def video_generator(input: UserMemory):
    """
    Endpoint to generate a video based on user-provided memory using Allegro's API.
    """
    try:
        response = requests.post(
            "https://api.rhymes.ai/v1/chat/completions",
            json={
                "api_key": ALLEGRO_API_KEY,
                "text": input.memory,
            }
        )
        response.raise_for_status()
        return {"video_url": response.json()["url"]}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
