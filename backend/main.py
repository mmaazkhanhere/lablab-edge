import os
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from models.emotion_therapy import emotion_therapy
# from models.prompt_for_image_generation import prompt_for_images
# from models.prompt_for_music_generation import prompt_for_music
# from models.image_generation import image_generation
# from models.music_generation import generate_music

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

app.mount("/images", StaticFiles(directory="generated_images"), name="images")
app.mount("/music", StaticFiles(directory="generated_music"), name="music")

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


# # image generation endpoint
# @app.post('/image')
# async def image_analyzer(input: UserMemory):
#     try:
#         prompt: str = prompt_for_images(input.memory)
#         image_response = image_generation(prompt, num_images=4)
#         if not image_response.get("image_urls"):
#             raise HTTPException(status_code=500, detail="No images were generated.")

#         return {"image_urls": image_response["image_urls"]}

#     except HTTPException as http_exc:
#         raise http_exc
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    

# # music generation endpoint
# @app.post('/music')
# async def music_generator(input: UserMemory):
#     """
#     Endpoint to generate music based on user-provided memory.
#     """

#     try:
#         prompt = prompt_for_music(input.memory)
#         audio_url = generate_music(prompt)
#         return MusicResponse(audio_url=audio_url)
#     except HTTPException as he:
#         raise he
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="An unexpected error occurred.")