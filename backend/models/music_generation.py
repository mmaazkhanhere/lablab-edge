import os
import requests
from fastapi import HTTPException
from dotenv import load_dotenv
import logging
import replicate

API_URL = "https://api.aimlapi.com/generate"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def generate_music(prompt: str) -> str:
    """
    Calls the external music generation API and returns the audio URL.
    """
    try:
        # Retrieve the Replicate API token from environment variables
        REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
        if not REPLICATE_API_TOKEN:
            logger.error("REPLICATE_API_TOKEN not found in environment variables.")
            raise HTTPException(status_code=500, detail="API token not configured.")
        
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
            api_token=os.getenv('REPLICATE_API_TOKEN') 
        )
            
        if not output:
            logger.error("Music generation failed.")
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

        logger.info(f"Music saved successfully at {music_path}")

        # Construct the full URL to access the music file
        # Assuming FastAPI is running on localhost:8000
        base_url = 'http://localhost:8000'
        return f"{base_url}/music/{music_filename}"

    except HTTPException as http_exc:
        logger.error(f"HTTPException: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))