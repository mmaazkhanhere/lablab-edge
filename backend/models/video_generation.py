import requests
import logging
import os
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_key = os.getenv('ALLEGRO_API_KEY')

def generate_video(request_id):
    if not api_key:
        logging.error("API key not found in environment variables.")
        raise ValueError("API_KEY not found in environment variables.")
    
    # First API call to get the video link
    url = "https://api.rhymes.ai/v1/videoQuery"
    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    params = {
        "requestId": request_id
    }

    try:
        # Get the video link from the first API call
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise exception for bad status codes
        
        response_data = response.json()
        if not response_data or 'data' not in response_data:
            logging.error("Invalid response format from the API")
            raise HTTPException(status_code=500, detail="Invalid API response format")
        
        video_url = response_data['data']
        if not video_url:
            logging.error("No video URL received from the API")
            raise HTTPException(status_code=500, detail="No video URL in response")

        # Download the video from the provided link
        video_response = requests.get(video_url, stream=True)
        video_response.raise_for_status()  # Raise exception for bad status codes

        # Create directory and save the video
        video_dir = './generated_videos'
        os.makedirs(video_dir, exist_ok=True)
        video_filename = f"generated_video_{request_id}.mp4"
        video_path = os.path.join(video_dir, video_filename)

        # Write the video content to file
        with open(video_path, 'wb') as file:
            for chunk in video_response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

        logger.info(f"Video downloaded and saved successfully at {video_path}")

        base_url = 'http://localhost:8000'
        return f"{base_url}/video/{video_filename}"

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Video generation failed: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")