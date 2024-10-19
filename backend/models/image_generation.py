import os
import requests
from fastapi import HTTPException
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def image_generation(memory: str) -> str:
    """
    Create a visual image based on the provided memory text.

    Args:
        memory (str): The input text describing the memory.

    Returns:
        str: The file path to the generated image.
    """
    api_key = os.getenv('API_KEY')
    if not api_key:
        logger.error("API_KEY not found in environment variables.")
        raise ValueError("API_KEY not found in environment variables.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": f"You will be provided a user memory: {memory}. Your task is to create a realistic image \
                   that visually represents this memory.",
        "model": "flux/dev",  # Ensure this is the correct model name as per API documentation
    }

    try:
        response = requests.post(
            "https://api.aimlapi.com/images/generations",
            headers=headers,
            json=payload
        )
        response.raise_for_status()  # Raise an error for bad status codes
        logger.info("Image generation request successful.")
    except requests.RequestException as e:
        logger.error(f"Image generation request failed: {e}")
        raise HTTPException(status_code=500, detail=f"Image generation failed: {e}")

    try:
        response_json = response.json()
        logger.info(f"API Response: {response_json}")  # Log the entire response for debugging

        # Extract the image URL from the 'images' key
        images = response_json.get("images")
        if not images or not isinstance(images, list):
            logger.error("No images found in the response.")
            raise HTTPException(status_code=500, detail="No images found in the response.")

        image_url = images[0].get("url")
        if not image_url:
            logger.error("Image URL not found in the response.")
            raise HTTPException(status_code=500, detail="Image URL not found in the response.")

        logger.info(f"Downloading image from URL: {image_url}")
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        image_data = image_response.content
    except (KeyError, IndexError, ValueError, requests.RequestException) as e:
        logger.error(f"Failed to process image data: {e}. Response JSON: {response_json}")
        raise HTTPException(status_code=500, detail=f"Failed to process image data: {e}. Response JSON: {response_json}")

    # Define the image file path
    image_path = "./generated_image.png"

    try:
        # Save the image to the specified path
        with open(image_path, "wb") as file:
            file.write(image_data)
        logger.info(f"Image saved successfully at {image_path}")
    except IOError as e:
        logger.error(f"Failed to save image: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save image: {e}")

    return image_path
