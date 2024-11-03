import os
import requests

ARIA_API_KEY = os.getenv('ARIA_API_KEY')

def image_generation(prompt: str, num_images: int = 4):
    """
    Generates images using the Aria API.
    """
    response = requests.post(
        "https://aria-api.com/generate_image",
        json={
            "api_key": ARIA_API_KEY,
            "prompt": prompt,
            "num_images": num_images,
        },
    )
    response.raise_for_status()
    return response.json()
