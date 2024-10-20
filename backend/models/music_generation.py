import os
import requests
from fastapi import HTTPException
from dotenv import load_dotenv
import logging
import replicate

API_URL = "https://api.aimlapi.com/generate"


load_dotenv()

def generate_music(prompt: str) -> str:
    """
    Calls the external music generation API and returns the audio URL.
    """
    try:

        REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
        if not REPLICATE_API_TOKEN:
            logging.error("API token not found in environment.")
            raise HTTPException(status_code=500, detail="API token not configured.")
        else:
            logging.info(f"Using API token: {REPLICATE_API_TOKEN}")
        
        input_data = {
            "prompt": prompt,
            "model_version": "melody",
            "output_format": "mp3",
            "normalization_strategy": "peak"
        }
        
        # Call the Replicate API to generate music
        output = replicate.run(
            "facebookresearch/musicgen:7a76a8258b23fae65c5a22debb8841d1d7e816b75c2f24218cd2bd8573787906",
            input=input_data,
            REPLICATE_API_TOKEN=os.getenv('REPLICATE_API_TOKEN')  
        )
            
        if not output:
            raise HTTPException(status_code=500, detail="Music generation failed.")

        # Step 3: Save music file
        music_dir = "./generated_music"
        os.makedirs(music_dir, exist_ok=True)
        music_filename = f"generated_music_1.mp3"
        music_path = os.path.join(music_dir, music_filename)

        # Download music from the provided URL
        response = requests.get(output)
        response.raise_for_status()
        with open(music_path, "wb") as file:
            file.write(response.content)

        # Construct the full URL to access the music file
        base_url = 'http://localhost:8000'
        return f"{base_url}/music/{music_filename}"

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))