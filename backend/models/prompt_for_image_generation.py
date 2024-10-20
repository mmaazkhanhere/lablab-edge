import os
from dotenv import load_dotenv

from openai import OpenAI
from openai.types.chat import ChatCompletion

load_dotenv()

client: OpenAI = OpenAI(
    api_key=os.getenv('API_KEY'),
    base_url='https://api.aimlapi.com'
)

def prompt_for_images(memory: str)-> str:
    """
    Recieves a memory from user, which is processed by AI and returns a prompt that can be used
    by AI models to create image and music that can heal user emotionally
    
    Arguments:
        memory (str): The memory from the user
        
    Return:
        prompt (str): A prompt that can be used by AI models to create image and music that can heal 
                        user emotionally

    """
    
    response: ChatCompletion = client.chat.completions.create(
    model ="meta-llama/Llama-3.2-3B-Instruct-Turbo",
    messages=[
            {
                "role": "system", 
                "content": f"""You are an AI designed to create prompts for an image generation model based 
                on a user’s emotional memory {memory}. Your task is to ensure that the generated image 
                accurately reflects the memory’s specific details and emotional atmosphere. Analyze the 
                memory for key visual elements such as people, places, objects, and activities, along with 
                the emotional tone, whether it be nostalgia, joy, peace, or any other feeling. Your prompt 
                should clearly describe these elements, including settings, individuals involved, and any 
                significant objects, while conveying the right mood through the description of lighting, 
                colors, and overall atmosphere. The goal is to guide the model to create an image that not 
                only mirrors the memory but also evokes the emotions tied to it, with sufficient detail to 
                reflect both the context and the emotional depth of the user's recollection."""
            },
            {
                "role": "user", 
                "content": memory
            }
        ]   
    )
    
    prompt: str = response.choices[0].message.content
    return prompt