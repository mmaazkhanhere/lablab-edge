import time
import requests
import logging
import os
from fastapi import HTTPException


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_RETRIES = 4
RETRY_DELAY = 130  # Seconds

api_key = os.getenv('ALLEGRO_API_KEY')

def generate_video(request_id: str):
    logger.info(f"Generating video for request ID: {request_id}")

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

    for retry_count in range(MAX_RETRIES):
        try:
            # Get the video link from the first API call
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raise exception for bad status codes
            
            response_data = response.json()
            if 'error' in response_data:
                logging.error(f"API returned an error: {response_data['error']}")
                raise HTTPException(status_code=500, detail=response_data['error'])
            elif 'data' in response_data and response_data['data']:
                video_url = response_data['data']
                break  # Exit the loop if we got a valid video URL
            else:
                logging.error("No video URL received from the API")
                if retry_count < MAX_RETRIES - 1:
                    logging.info(f"Retrying in {RETRY_DELAY} seconds...")
                    time.sleep(RETRY_DELAY)
                else:
                    raise HTTPException(status_code=500, detail="No video URL in response")
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {str(e)}")
            if retry_count < MAX_RETRIES - 1:
                logging.info(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                raise HTTPException(status_code=500, detail=f"Video generation failed: {str(e)}")
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            if retry_count < MAX_RETRIES - 1:
                logging.info(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    # Download the video from the provided link
    video_response = requests.get(video_url, stream=True)
    video_response.raise_for_status()  # Raise exception for bad status codes

    # Create directory and save the video
    video_dir = './generated_videos'
    os.makedirs(video_dir, exist_ok=True)
    video_filename = f"generated_video_1.mp4"
    video_path = os.path.join(video_dir, video_filename)

    # Write the video content to file
    with open(video_path, 'wb') as file:
        for chunk in video_response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

    logger.info(f"Video downloaded and saved successfully at {video_path}")

    base_url = 'http://localhost:8000'
    return f"{base_url}/videos/{video_filename}"