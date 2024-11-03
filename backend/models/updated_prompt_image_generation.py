import os
from dotenv import load_dotenv

from openai import OpenAI
from openai.types.chat import ChatCompletion

load_dotenv()

client: OpenAI = OpenAI(
    api_key=os.getenv('ARIA_API_KEY'),
    base_url='https://api.aria.com'
)

def prompt_for_images(memory: str) -> str:
    """
    Recieves a memory from user and returns a prompt for image generation.
    
    Arguments:
        memory (str): The memory from the user
        
    Return:
        prompt (str): A prompt for AI to generate soothing and relevant images.
    """
    
    response: ChatCompletion = client.chat.completions.create(
        model="aria-mixture-of-experts",
        messages=[
            {
                "role": "system", 
                "content": f"""You are an AI that creates prompts for an image generation model. Use the user’s memory \"{memory}\" 
                to generate descriptions for soothing images that align with emotional healing. Provide specific visual elements that 
                convey comfort, closure, peace, or joy, depending on the memory's sentiment."""
            },
            {
                "role": "user", 
                "content": memory
            }
        ]
    )
    
    prompt: str = response.choices[0].message.content
    return prompt
