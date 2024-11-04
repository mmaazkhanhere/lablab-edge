import os
import logging
import logging 

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from models.emotion_therapy import emotion_therapy
from models.prompt_for_image_generation import prompt_for_images
from models.prompt_for_music_generation import prompt_for_music
from models.image_generation import image_generation
from models.music_generation import generate_music
from models.video_generation_request import generate_video_request
from models.video_generation import generate_video


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class UserMemory(BaseModel):
    memory: str
    
class EmotionallyTherapyResponse(BaseModel):
    ai_response: str
    
class MusicResponse(BaseModel):
    audio_url: str  
    
class MusicResponse(BaseModel):
    audio_url: str  

class VideoIDResponse(BaseModel):
    message: str
    data: str
    status: int 

class VideoResponse(BaseModel):
    video_url: str

app: FastAPI = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/images", StaticFiles(directory="generated_images"), name="images")
app.mount("/music", StaticFiles(directory="generated_music"), name="music")
app.mount("/music", StaticFiles(directory="generated_music"), name="music")
app.mount("/videos", StaticFiles(directory="generated_videos"), name="videos")

@app.get("/")
async def root():
    return {"message": "Revisit: "}

# emotional therapy api endpoint
@app.post('/emotion-therapy')
async def memory_emotional_therapy(request: Request):
    # response  = emotion_therapy(input.memory)
    # return response
    data = await request.json()
    memory = data.get("memory")
    return StreamingResponse(emotion_therapy(memory), media_type="text/plain")


# image generation endpoint
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
    

# music generation endpoint
@app.post('/music')
async def music_generator(input: UserMemory):
    """
    Endpoint to generate music based on user-provided memory.
    """

    try:
        prompt = prompt_for_music(input.memory)
        audio_url = generate_music(prompt)
        return MusicResponse(audio_url=audio_url)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
    

@app.post('/video')
async def video_generator(input: UserMemory):
    """
    Endpoint to generate video based on user-provided memory.
    Returns video details including local path and URL.
    """
    try:
        video_request_id = generate_video_request(input.memory)
        logger.info(f"Video Request Generated {video_request_id}")

        request_id: str = video_request_id["data"]  
        logger.info(f"Video Request ID: {request_id}")
        
        video_url = generate_video(request_id)
        # video_url = generate_video("cf3488a4-ed4b-45f0-807b-d9db014fd69d")
        logger.info("Video URL Generated")
        return VideoResponse(video_url=video_url)
        
    except HTTPException as he:
        # Re-raise HTTP exceptions with their original status code and detail
        raise he
    except Exception as e:
        # Convert unexpected exceptions to 500 Internal Server Error
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
