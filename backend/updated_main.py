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

from fastapi.responses import FileResponse
import uuid

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
video_dir = os.path.join(current_dir, "generated_videos")
os.makedirs(video_dir, exist_ok=True)

app.mount("/images", StaticFiles(directory=images_dir), name="images")
app.mount("/music", StaticFiles(directory=music_dir), name="music")
app.mount("/videos", StaticFiles(directory=video_dir), name="videos")
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
    """
    Endpoint to generate a video based on user-provided memory and save it locally.
    """
    try:
        video_data = generate_video(ALLEGRO_API_KEY)  # Call your video generation function
        
        # Simulate downloading the video file (assuming the response contains a URL to the video file)
        video_url = video_data.get("video_url")
        if not video_url:
            raise HTTPException(status_code=500, detail="No video was generated.")

        # Download the video content
        video_content = requests.get(video_url).content

        # Generate a unique filename for the video
        video_filename = f"{uuid.uuid4()}.mp4"
        video_path = os.path.join(video_dir, video_filename)

        # Save the video to the local directory
        with open(video_path, "wb") as video_file:
            video_file.write(video_content)

        return {"video_url": f"/videos/{video_filename}"}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))







