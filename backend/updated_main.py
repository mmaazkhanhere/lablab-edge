from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from models.updated_prompt_image_generation import prompt_for_images
from models.prompt_for_music_generation import prompt_for_music
from models.updated_image_generation import image_generation
from models.music_generation import generate_music
from models.emotion_therapy import emotion_therapy
from models.video_generation import generate_video

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
async def memory_emotional_therapy(input: UserMemory, response_model=EmotionallyTherapyResponse):
    # logging.info("Emotion therapy endpoint called.")
    response: EmotionallyTherapyResponse = emotion_therapy(input.memory)
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
    try:
        # Call the generate_video function with the token and prompt
        video_response = generate_video(ALLEGRO_API_KEY, input.memory)
        
        if "error" in video_response:
            raise HTTPException(status_code=500, detail=video_response["error"])
        
        return {"video_url": video_response.get("url")}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))







