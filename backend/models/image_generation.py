import os
import requests

from fastapi import HTTPException

from dotenv import load_dotenv

load_dotenv()

def image_generation(prompt: str, num_images: int = 5) -> dict:
    """
    Create visual images based on the provided memory text.

    Args:
        prompt (str): The input text describing the memory.
        num_images (int): Number of images to generate.

    Returns:
        dict: Dictionary containing lists of image file paths and URLs.
    """
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY not found in environment variables.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"Create a visually soothing image that represents the emotional tone of the provided memory {prompt}, using calming elements like nature, light, and colors to evoke healing and peace"

    images_dir = "./generated_images"
    os.makedirs(images_dir, exist_ok=True)

    saved_image_paths = []

    # Generate images one by one in a loop
    for i in range(num_images):
        payload = {
            "prompt": prompt,
            "model": "flux/dev"
        }

        try:
            response = requests.post(
                "https://api.aimlapi.com/images/generations",
                headers=headers,
                json=payload
            )
            response.raise_for_status()  
        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Image generation failed: {e}")

        try:
            response_json = response.json()

            # Extract the image URLs from the 'images' key
            images = response_json.get("images")
            if not images or not isinstance(images, list):
                raise HTTPException(status_code=500, detail="No images found in the response.")

            image_url = images[0].get("url")
            if not image_url:
                raise HTTPException(status_code=500, detail="Image URL not found in the response.")

            # Download and save the image
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            image_data = image_response.content

            # Generate fixed filename using loop index to overwrite existing images
            image_filename = f"generated_image_{i}.png" 
            image_path = os.path.join(images_dir, image_filename)

            # Save the image, overwriting if it already exists
            with open(image_path, "wb") as file:
                file.write(image_data)
            saved_image_paths.append(image_path)

        except (KeyError, IndexError, ValueError, requests.RequestException) as e:
            raise HTTPException(status_code=500, detail=f"Failed to process image data: {e}. Response JSON: {response_json}")

    image_urls_local = [f"/images/{os.path.basename(path)}" for path in saved_image_paths]
    return {"image_paths": saved_image_paths, "image_urls": image_urls_local}
