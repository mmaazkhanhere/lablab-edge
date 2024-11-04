import os
import requests
import logging
from fastapi import HTTPException
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_key = os.getenv('ALLEGRO_API_KEY')

def generate_video_request(prompt):

    if not api_key:
        logging.error("API key not found in environment variables.")
        raise ValueError("API_KEY not found in environment variables.")

    url = "https://api.rhymes.ai/v1/generateVideoSyn"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "refined_prompt": prompt,
        "num_step": 100,
        "cfg_scale": 7.5,
        "user_prompt": prompt,
        "rand_seed": 12345
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        # Check if the request was successful
        response.raise_for_status()
        return response.json()  # Return the JSON response
    except requests.exceptions.RequestException as e:
        logger.error(f"[REQUEST_FAILED]: {str(e)}")
        return f"An error occurred: {str(e)}"